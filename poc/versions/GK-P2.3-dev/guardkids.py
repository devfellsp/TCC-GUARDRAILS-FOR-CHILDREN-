"""POC local: corpus selecionado, RAG e verificações contextuais com Qwen3."""
from __future__ import annotations

import argparse
import hashlib
import json
import io
import os
import platform
import re
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from importlib.metadata import distributions

import httpx
import numpy as np
from pydantic import BaseModel, ConfigDict, Field
from settings import Settings
from privacy import contains_private_data, log_record
from channels import CHANNELS
from response_styles import RESPONSE_STYLES

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]  # TCC/poc/versions/GK-P2.3-dev; estado isolado por versão.
LOCK = threading.Lock()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def config():
    return Settings.model_validate(read_json(BASE / "config.json")).model_dump()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


class BusyError(RuntimeError):
    pass


class PersistenceError(RuntimeError):
    pass


class Classification(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    category: Literal["normal", "danger", "self_harm", "sexual", "hate", "substance", "privacy", "prompt_injection"]
    needs_protection: bool
    educational_predation: bool
    help_seeking: bool
    reason: str = Field(min_length=1, max_length=600)


class Generation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    supported: bool
    answer: str = Field(max_length=3000)
    source_ids: list[str]


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    source_id: str
    quote: str = Field(min_length=8, max_length=850)


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    text: str = Field(min_length=1, max_length=500)
    evidence: list[Evidence] = Field(min_length=1, max_length=3)


class Draft(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    supported: bool
    claims: list[Claim] = Field(max_length=3)


class ClaimVerdict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    claim: int = Field(ge=1, le=3)
    supported: bool
    reason: str = Field(min_length=1, max_length=250)


class Grounding(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    claims: list[ClaimVerdict] = Field(max_length=3)
    answers_question: bool
    language_ok: bool
    reason: str = Field(min_length=1, max_length=600)


def decision(result, policy):
    if result.needs_protection:
        return "safe_guidance" if (result.category in {"self_harm", "privacy"} or
                                   (result.help_seeking and result.category in {"danger", "sexual", "hate", "substance"})) else "block"
    if result.educational_predation and not policy["allow_educational_predation"]:
        return "block"
    return "allow"


MESSAGES = {
    "block": "Não posso ajudar com esse pedido. Podemos aprender e conversar de forma segura e respeitosa.",
    "self_harm": "Se você está sofrendo ou pensando em se machucar, procure agora um adulto de confiança, como um responsável ou professor. Você merece cuidado e companhia.",
    "privacy": "Para proteger você, não compartilhe nome completo, endereço, escola, telefone ou outros dados pessoais aqui. Podemos estudar sem essas informações.",
    "hate": "Você merece ser tratado com respeito. Se alguém está ofendendo ou humilhando você, procure um adulto de confiança, como um responsável ou professor. Não é preciso repetir as ofensas nem informar nomes aqui.",
    "substance": "Se você está preocupado com bebidas, drogas ou remédios, converse com um adulto de confiança. Não experimente nem use remédios por conta própria. Você pode pedir ajuda sem dar nomes ou outros dados pessoais aqui.",
    "danger": "Se alguém ameaçou você ou existe algum perigo, vá para um lugar seguro se puder e procure agora um adulto de confiança, como um responsável ou professor. Conte o que aconteceu e peça para ficar acompanhado. Não confronte a pessoa. Se o perigo estiver acontecendo agora, peça ao adulto para buscar ajuda de emergência. Você não precisa informar nomes ou endereço aqui.",
    "sexual": "Se uma situação ou conversa deixa você desconfortável, conte a um adulto de confiança e peça ajuda. Você pode falar sobre seu desconforto sem descrever detalhes íntimos ou informar nomes aqui.",
    "redirect": "Não encontrei no acervo deste chat uma base suficiente para responder. Você pode tentar outra pergunta ou escolher outro chat.",
    "technical_error": "Não consegui concluir esta tentativa. Peça ao pesquisador para verificar o funcionamento e tente novamente.",
}


class Ollama:
    def __init__(self, cfg, deadline=None, cancelled=None):
        self.cfg = cfg
        self.calls = []
        self.deadline = deadline or time.monotonic() + cfg["runtime"]["deadline_seconds"]
        self.cancelled = cancelled or threading.Event()
        self._identities = None

    def check_budget(self):
        if self.cancelled.is_set():
            raise TimeoutError("Execucao cancelada")
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Prazo total excedido")
        return remaining

    def request(self, endpoint, payload=None):
        url = self.cfg["ollama_url"] + endpoint
        remaining = self.check_budget()
        with httpx.Client(timeout=remaining, trust_env=False) as client:
            with client.stream("GET" if payload is None else "POST", url, json=payload) as response:
                response.raise_for_status()
                body = bytearray()
                for part in response.iter_bytes():
                    self.check_budget()
                    body.extend(part)
                    if len(body) > 8_000_000:
                        raise ValueError("Resposta do servico excede o limite")
                self.check_budget()
                return json.loads(body)

    def identities(self):
        if self._identities is None:
            self._identities = {m["name"]: m["digest"] for m in self.request("/api/tags")["models"]}
        return self._identities

    def embed(self, texts):
        started = time.perf_counter()
        result = self.request("/api/embed", {
            "model": self.cfg["embedding_model"], "input": texts,
            "truncate": False, "keep_alive": "5m", "options": {"num_gpu": 0},
        })
        self.calls.append({"stage": "embedding", "seconds": round(time.perf_counter() - started, 3)})
        vectors = np.asarray(result["embeddings"], dtype=np.float32)
        if vectors.ndim != 2 or len(vectors) != len(texts) or not np.isfinite(vectors).all():
            raise ValueError("Embedding inválido")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        if np.any(norms == 0):
            raise ValueError("Embedding nulo")
        return vectors / norms

    def structured(self, prompt_name, data, schema, stage):
        prompt = (BASE / "prompts" / prompt_name).read_text(encoding="utf-8")
        if stage == "generation":
            # Somente instruções locais aprovadas entram no prompt de sistema.
            prompt += "\nPolítica de linguagem:\n" + RESPONSE_STYLES[data.get("response_style", "padrao")]["instruction"]
        started = time.perf_counter()
        options = dict(self.cfg["generation"])
        if stage != "generation":
            options["num_predict"] = 550 if stage == "grounding_guard" else 240
        result = self.request("/api/chat", {
            "model": self.cfg["model"], "stream": False, "think": False,
            "format": schema.model_json_schema(), "options": options, "keep_alive": "10m",
            "messages": [{"role": "system", "content": prompt},
                         {"role": "user", "content": json.dumps(data, ensure_ascii=False)}],
        })
        self.calls.append({"stage": stage, "seconds": round(time.perf_counter() - started, 3),
                           "eval_count": result.get("eval_count"),
                           "prompt_eval_count": result.get("prompt_eval_count"),
                           "done_reason": result.get("done_reason")})
        if result.get("done_reason") == "length":
            raise ValueError(f"Resposta truncada no estágio {stage}")
        return schema.model_validate_json(result["message"]["content"])


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


def split_passage(text, max_chars, overlap=1):
    if max_chars <= 0 or overlap < 0:
        raise ValueError("Fragmentacao invalida")
    sentences = []
    for sentence in re.split(r"(?<=[.!?])\s+", clean(text)):
        # Sentencas isoladas grandes tambem respeitam o limite rigido.
        while len(sentence) > max_chars:
            boundary = sentence.rfind(" ", 0, max_chars + 1)
            boundary = boundary if boundary > 0 else max_chars
            sentences.append(sentence[:boundary])
            sentence = sentence[boundary:].lstrip()
        if sentence:
            sentences.append(sentence)
    chunks, current = [], []
    for sentence in sentences:
        if current and len(" ".join(current + [sentence])) > max_chars:
            chunks.append(" ".join(current))
            current = current[-overlap:] if overlap else []
            while current and len(" ".join(current + [sentence])) > max_chars:
                current.pop(0)
        current.append(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks


def extract_corpus(cfg):
    from pypdf import PdfReader
    manifest = read_json(BASE / "corpus_manifest.json")
    chunks, source_hashes = [], {}
    for source in manifest["sources"]:
        channel = source.get("channel")
        if channel not in CHANNELS:
            raise ValueError("Disciplina explícita e válida obrigatória para cada fonte")
        path = ROOT / source["file"]
        if not path.resolve().is_relative_to(ROOT.resolve()) or path.suffix.lower() not in {".pdf", ".txt"}:
            raise ValueError("A fonte deve ser um PDF ou texto dentro do projeto")
        source_hashes[source["id"]] = digest(path.read_bytes())
        if source_hashes[source["id"]] != source.get("source_sha256"):
            raise ValueError("Arquivo da fonte difere do manifesto conferido")
        if path.suffix.lower() == ".txt":
            for i, part in enumerate(split_passage(path.read_text(encoding="utf-8"), cfg["retrieval"]["chunk_chars"], cfg["retrieval"]["overlap_sentences"])):
                chunks.append({"id": f"{source['id']}-t{i + 1}", "source": source["title"],
                               "file": source["file"], "channel": source["channel"],
                               "pdf_page": None, "printed_page": None, "text": part})
            continue
        reader = PdfReader(path)
        for passage in source["passages"]:
            text = clean(reader.pages[passage["pdf_page"] - 1].extract_text())
            start = clean(passage["start"])
            if start not in text:
                raise ValueError(f"Âncora inicial não encontrada: {source['id']} p.{passage['pdf_page']}")
            text = text[text.index(start):]
            if passage.get("end"):
                end = clean(passage["end"])
                if end not in text:
                    raise ValueError("Âncora final não encontrada")
                text = text[:text.index(end)]
            text = clean(text)
            if passage.get("text_sha256") and digest(text.encode("utf-8")) != passage["text_sha256"]:
                raise ValueError("Recorte difere da transcrição conferida")
            if len(text) < 80:
                raise ValueError("Trecho insuficiente")
            for i, part in enumerate(split_passage(text, cfg["retrieval"]["chunk_chars"], cfg["retrieval"]["overlap_sentences"])):
                identifier = passage.get("id", f"{source['id']}-p{passage['printed_page']}")
                chunks.append({"id": f"{identifier}-{i + 1}",
                               "source": source["title"], "file": source["file"],
                               "pdf_page": passage["pdf_page"], "printed_page": passage["printed_page"],
                               "text": part, "channel": channel})
    if len({c["id"] for c in chunks}) != len(chunks):
        raise ValueError("Identificadores duplicados no acervo")
    return chunks, manifest, source_hashes


def build_index():
    cfg = config()
    chunks, manifest, source_hashes = extract_corpus(cfg)
    client = Ollama(cfg)
    identities = client.identities()
    vectors = client.embed([c["text"] for c in chunks])
    meta = {"created_at": datetime.now(timezone.utc).isoformat(), "chunks": chunks,
            "embedding_model": cfg["embedding_model"], "embedding_digest": identities[cfg["embedding_model"]],
            "retrieval": cfg["retrieval"], "manifest_hash": digest(manifest), "source_hashes": source_hashes,
            "vector_hash": digest(vectors.tobytes()), "calls": client.calls}
    publish_index(meta, vectors)
    print(json.dumps({"chunks": len(chunks), "dimensions": vectors.shape[1], "calls": client.calls}, ensure_ascii=False))


def publish_index(meta, vectors):
    identifier = digest(meta)
    folder = BASE / "data" / "indices" / identifier
    folder.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO()
    np.savez_compressed(buffer, vectors=vectors)
    vector_path = folder / "index.npz"
    if vector_path.exists():
        with np.load(vector_path, allow_pickle=False) as existing:
            if digest(existing["vectors"].tobytes()) != meta["vector_hash"]:
                raise ValueError("A versao existente do indice foi alterada; reconstrua a base.")
    if not vector_path.exists():
        temp = folder / f".{uuid.uuid4().hex}.tmp"
        try:
            temp.write_bytes(buffer.getvalue())
            os.replace(temp, vector_path)
        finally:
            temp.unlink(missing_ok=True)
    atomic_json(folder / "chunks.json", meta)
    # Leitores continuam usando a versao anterior ate que os dois arquivos estejam completos.
    atomic_json(BASE / "data" / "current.json", {"id": identifier})
    return identifier


def validate_index(meta, vectors, cfg, identities=None):
    if meta["manifest_hash"] != digest(read_json(BASE / "corpus_manifest.json")) or meta["retrieval"] != cfg["retrieval"]:
        raise ValueError("Acervo ou parâmetros alterados; reconstrua o índice.")
    if (meta["embedding_model"] != cfg["embedding_model"] or
            (identities is not None and meta["embedding_digest"] != identities.get(cfg["embedding_model"]))):
        raise ValueError("Modelo de embeddings alterado; reconstrua o índice.")
    actual_chunks, _, source_hashes = extract_corpus(cfg)
    canonical = lambda chunks: [dict(c, text=clean(c["text"])) for c in chunks]
    if canonical(actual_chunks) != canonical(meta["chunks"]) or source_hashes != meta["source_hashes"]:
        raise ValueError("Texto, metadados ou PDF divergem do acervo; reconstrua o indice.")
    if (vectors.ndim != 2 or not len(vectors) or not vectors.shape[1] or not np.isfinite(vectors).all()
            or digest(vectors.tobytes()) != meta["vector_hash"] or len(vectors) != len(meta["chunks"])
            or not np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-5)):
        raise ValueError("Índice inconsistente")


def load_index(cfg, identities=None):
    pointer = read_json(BASE / "data" / "current.json")
    identifier = pointer["id"]
    if not isinstance(identifier, str) or not re.fullmatch(r"[0-9a-f]{64}", identifier):
        raise ValueError("Identificador de indice invalido")
    folder = BASE / "data" / "indices" / identifier
    meta = read_json(folder / "chunks.json")
    if digest(meta) != identifier:
        raise ValueError("Metadados alterados")
    with np.load(folder / "index.npz", allow_pickle=False) as index:
        vectors = index["vectors"]
    validate_index(meta, vectors, cfg, identities)
    return meta, vectors, identifier


def migrate_index():
    """Valida os dados legados contra os PDFs antes de publica-los; sem inferencia."""
    cfg = config()
    meta = read_json(BASE / "data" / "chunks.json")
    with np.load(BASE / "data" / "index.npz", allow_pickle=False) as index:
        vectors = index["vectors"]
    validate_index(meta, vectors, cfg)
    return publish_index(meta, vectors)


def retrieve(question, cfg, client, channel="ciencias"):
    if channel not in CHANNELS:
        raise ValueError("Chat desconhecido")
    meta, vectors, identifier = load_index(cfg, client.identities())
    client.check_budget()
    query = client.embed([question])[0]
    if query.shape != (vectors.shape[1],):
        raise ValueError("Dimensao de embeddings incompatível")
    scores = vectors @ query
    # Filtrar antes do top-k evita que fontes de outro chat ocupem as vagas.
    eligible = [i for i, chunk in enumerate(meta["chunks"]) if chunk.get("channel", "ciencias") == channel]
    order = sorted(eligible, key=lambda i: -float(scores[i]))[:cfg["retrieval"]["top_k"]]
    selected = [dict(meta["chunks"][int(i)], score=round(float(scores[i]), 6)) for i in order
                if scores[i] >= cfg["retrieval"]["min_similarity"]]
    return selected, identifier


def protected_message(action, result, question=""):
    # Defesa adicional para relatos de ameaça classificados como humilhação.
    # Não substitui a classificação de intenção nem transforma pedidos de dano em ajuda.
    if (action == "safe_guidance" and result.help_seeking and result.category in {"danger", "hate"}
            and re.search(r"\bamea[çc]\w*", question, re.IGNORECASE)):
        return MESSAGES["danger"]
    return MESSAGES[result.category] if action == "safe_guidance" else MESSAGES["block"]


def assemble_draft(draft, chunks, response_style):
    """Só monta afirmações cujas citações literais existem nas fontes recuperadas."""
    if not draft.supported or not draft.claims:
        return None
    sources = {c["id"]: c["text"] for c in chunks}
    identifiers = []
    for claim in draft.claims:
        if not claim.text.strip():
            return None
        for evidence in claim.evidence:
            if evidence.source_id not in sources or clean(evidence.quote) not in clean(sources[evidence.source_id]):
                return None
            if evidence.source_id not in identifiers:
                identifiers.append(evidence.source_id)
    parts = [c.text.strip() for c in draft.claims]
    answer = ("\n".join(f"{i}. {text}" for i, text in enumerate(parts, 1))
              if response_style == "passo_a_passo" else " ".join(parts))
    if len(answer.split()) > 120:
        return None
    return Generation(supported=True, answer=answer, source_ids=identifiers)


def grounding_accepts(grounding, draft):
    numbers = [v.claim for v in grounding.claims]
    return (len(numbers) == len(draft.claims) and set(numbers) == set(range(1, len(draft.claims) + 1))
            and all(v.supported for v in grounding.claims)
            and grounding.answers_question and grounding.language_ok)


def save_snapshot(cfg):
    snapshot = {"configuration": cfg, "manifest": read_json(BASE / "corpus_manifest.json"),
                "channels": CHANNELS,
                "response_styles": RESPONSE_STYLES,
                "prompts": {p.name: p.read_text(encoding="utf-8") for p in (BASE / "prompts").glob("*.txt")},
                "implementation": {str(p.relative_to(BASE)): p.read_text(encoding="utf-8-sig")
                                   for p in sorted([*BASE.glob("*.py"), *BASE.glob("*.ps1"), *BASE.glob("*.cmd"),
                                                    *BASE.glob("web/*.html")])},
                "dependencies_lock": (BASE / "requirements-lock.txt").read_text(encoding="utf-8-sig"),
                "runtime": {"python": sys.version, "platform": platform.platform(),
                            "packages": dict(sorted((d.metadata["Name"], d.version) for d in distributions() if d.metadata["Name"]))}}
    try:
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                  text=True, timeout=3, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        revision = None
    snapshot["git_commit"] = revision
    if (BASE / "data" / "current.json").exists():
        meta, vectors, identifier = load_index(cfg)
        snapshot["index"] = {"id": identifier, "metadata": meta,
                             "vectors": vectors.tolist(), "dtype": str(vectors.dtype)}
    else:
        snapshot["index"] = None
    identifier = digest(snapshot)
    folder = BASE / "runs" / "snapshots"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{identifier}.json"
    if not path.exists():
        atomic_json(path, snapshot)
    return identifier


def run_question(question, policy_name=None, case_id=None, group="manual", split="development", *, synthetic=False, cancelled=None, channel="ciencias", response_style="padrao"):
    if channel not in CHANNELS:
        raise ValueError("Chat desconhecido")
    if response_style not in RESPONSE_STYLES:
        raise ValueError("Estilo de resposta desconhecido")
    if not isinstance(question, str) or not 1 <= len(question.strip()) <= 1500:
        raise ValueError("A pergunta deve conter de 1 a 1500 caracteres.")
    if not LOCK.acquire(blocking=False):
        raise BusyError("Ha uma execucao em andamento. Aguarde e tente novamente.")
    try:
        return _run(question.strip(), policy_name, case_id, group, split, synthetic, cancelled, channel, response_style)
    finally:
        LOCK.release()


def _run(question, policy_name, case_id, group, split, synthetic=False, cancelled=None, channel="ciencias", response_style="padrao"):
    cfg = config()
    name = policy_name or cfg["default_policy"]
    if name not in cfg["policies"]:
        raise ValueError("Configuração desconhecida")
    client = Ollama(cfg, cancelled=cancelled)
    started = time.perf_counter()
    record = {"id": uuid.uuid4().hex, "time_utc": datetime.now(timezone.utc).isoformat(),
              "question": question, "case_id": case_id, "group": group, "split": split, "channel": channel,
              "response_style": response_style, "response_style_hash": digest(RESPONSE_STYLES[response_style]),
              "policy": name, "configuration": cfg, "config_hash": digest(cfg),
              "prompt_hashes": {p.name: digest(p.read_bytes()) for p in (BASE / "prompts").glob("*.txt")},
              "implementation_hash": digest(Path(__file__).read_bytes()),
              "retrieved": [], "input_guard": None, "output_guard": None,
              "generated": None, "grounding_guard": None, "valid": False, "synthetic": synthetic}
    try:
        record["snapshot"] = save_snapshot(cfg)
        if contains_private_data(question):
            incoming = Classification(category="privacy", needs_protection=True,
                                      educational_predation=False, help_seeking=False, reason="Identificador pessoal explicito detectado localmente")
        else:
            record["model_digests"] = client.identities()
            record["ollama_version"] = client.request("/api/version").get("version")
            incoming = client.structured("classifier.txt", {"stage": "entrada", "channel": channel, "question": question}, Classification, "input_guard")
        action = decision(incoming, cfg["policies"][name])
        record["input_guard"] = dict(incoming.model_dump(), decision=action)
        if action != "allow":
            record.update(action=action, answer=protected_message(action, incoming, question), final_origin="input_guard")
        else:
            chunks, index_hash = retrieve(question, cfg, client, channel)
            record.update(retrieved=chunks, index_hash=index_hash)
            if not chunks:
                record.update(action="redirect", answer=MESSAGES["redirect"], final_origin="retrieval")
            else:
                draft = client.structured("generator.txt", {"profile": cfg["profile"], "channel": channel, "scope": CHANNELS[channel]["scope"], "response_style": response_style, "question": question, "sources": chunks}, Draft, "generation")
                record["draft"] = draft.model_dump()
                generated = assemble_draft(draft, chunks, response_style)
                record["generated"] = generated.model_dump() if generated else None
                if not draft.supported:
                    record.update(action="redirect", answer=MESSAGES["redirect"], final_origin="model_insufficient_support")
                elif generated is None:
                    record.update(action="redirect", answer=MESSAGES["redirect"], final_origin="evidence_guard")
                elif contains_private_data(generated.answer):
                    outgoing = Classification(category="privacy", needs_protection=True, educational_predation=False, help_seeking=False,
                                              reason="Identificador pessoal explicito detectado localmente na saida")
                    record["output_guard"] = dict(outgoing.model_dump(), decision="safe_guidance")
                    record.update(action="safe_guidance", answer=MESSAGES["privacy"], final_origin="output_guard")
                else:
                    grounding = client.structured("grounding.txt", {"question": question, "answer": generated.answer,
                                                     "claims": [dict(number=i, **c.model_dump()) for i, c in enumerate(draft.claims, 1)],
                                                     "sources": [c for c in chunks if c["id"] in generated.source_ids]},
                                                  Grounding, "grounding_guard")
                    accepted = grounding_accepts(grounding, draft)
                    record["grounding_guard"] = dict(grounding.model_dump(), supported=accepted)
                    if not accepted:
                        record.update(action="redirect", answer=MESSAGES["redirect"], final_origin="grounding_guard")
                    else:
                        outgoing = client.structured("classifier.txt", {"stage": "saída", "channel": channel, "question": question, "answer": generated.answer}, Classification, "output_guard")
                        action = decision(outgoing, cfg["policies"][name])
                        record["output_guard"] = dict(outgoing.model_dump(), decision=action)
                        record.update(action=action, answer=generated.answer if action == "allow" else protected_message(action, outgoing, question),
                                      final_origin="generation" if action == "allow" else "output_guard")
        client.check_budget()
        record["valid"] = True
    except Exception as exc:
        record.update(action="technical_error", answer=MESSAGES["technical_error"], error=type(exc).__name__, final_origin="technical_error")
    record["seconds"] = round(time.perf_counter() - started, 3)
    record["calls"] = client.calls
    logs = BASE / "runs"
    try:
        atomic_json(logs / f"{record['id']}.json", log_record(record, synthetic))
    except OSError as exc:
        raise PersistenceError("Nao foi possivel persistir o registro; resposta retida.") from exc
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["index", "migrate-index", "ask", "prune"])
    parser.add_argument("question", nargs="?")
    parser.add_argument("--policy", choices=list(config()["policies"]), default=None)
    parser.add_argument("--synthetic", action="store_true", help="Registrar texto integral: somente dados ficticios")
    parser.add_argument("--channel", choices=list(CHANNELS), default="ciencias")
    parser.add_argument("--response-style", choices=list(RESPONSE_STYLES), default="padrao")
    parser.add_argument("--apply", action="store_true", help="Aplicar expiracao de logs minimizados")
    args = parser.parse_args()
    if args.command == "index":
        build_index()
    elif args.command == "migrate-index":
        print(migrate_index())
    elif args.command == "prune":
        print(json.dumps(prune_logs(apply=args.apply)))
    elif args.question:
        result = run_question(args.question, args.policy, synthetic=args.synthetic, channel=args.channel, response_style=args.response_style)
        displayed = log_record(result, True) if args.synthetic else {
            key: result[key] for key in ["id", "answer", "action", "valid", "policy", "seconds"]}
        print(json.dumps(displayed, ensure_ascii=False, indent=2))
    else:
        parser.error("Informe a pergunta")


def prune_logs(apply=False):
    """Expira apenas logs minimizados novos; registros legados e de pesquisa sao preservados."""
    cutoff = datetime.now(timezone.utc).timestamp() - config()["runtime"]["retention_days"] * 86400
    selected = []
    for path in (BASE / "runs").glob("*.json"):
        try:
            record = read_json(path)
            if (record.get("logging_mode") == "minimized" and
                    datetime.fromisoformat(record["time_utc"]).timestamp() < cutoff):
                selected.append(path.name)
                if apply:
                    path.unlink()
        except (OSError, ValueError, KeyError):
            continue
    return {"files": selected, "applied": apply}


if __name__ == "__main__":
    main()
