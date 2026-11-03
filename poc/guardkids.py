"""POC local: corpus selecionado, RAG e verificações contextuais com Qwen3."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import httpx
import numpy as np
from pydantic import BaseModel, ConfigDict, Field

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
LOCK = threading.Lock()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def config():
    return read_json(BASE / "config.json")


class Classification(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    category: Literal["normal", "danger", "self_harm", "sexual", "hate", "substance", "privacy", "prompt_injection"]
    needs_protection: bool
    educational_predation: bool
    reason: str = Field(min_length=1, max_length=600)


class Generation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    supported: bool
    answer: str = Field(max_length=3000)
    source_ids: list[str]


def decision(result, policy):
    if result.needs_protection:
        return "safe_guidance" if result.category in {"self_harm", "privacy"} else "block"
    if result.educational_predation and not policy["allow_educational_predation"]:
        return "block"
    return "allow"


MESSAGES = {
    "block": "Não posso ajudar com esse pedido. Podemos conversar sobre os seres vivos e suas relações na natureza de forma segura.",
    "self_harm": "Se você está sofrendo ou pensando em se machucar, procure agora um adulto de confiança, como um responsável ou professor. Você merece cuidado e companhia.",
    "privacy": "Para proteger você, não compartilhe nome completo, endereço, escola, telefone ou outros dados pessoais aqui. Podemos estudar sem essas informações.",
    "redirect": "Não encontrei nos trechos selecionados uma base suficiente para responder. Podemos estudar alimentação dos seres vivos, cadeias alimentares e decomposição.",
    "technical_error": "Não consegui concluir esta tentativa. Peça ao pesquisador para verificar o funcionamento e tente novamente.",
}


class Ollama:
    def __init__(self, cfg):
        self.cfg = cfg
        self.calls = []

    def request(self, endpoint, payload=None):
        url = self.cfg["ollama_url"] + endpoint
        with httpx.Client(timeout=240, trust_env=False) as client:
            response = client.get(url) if payload is None else client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

    def identities(self):
        return {m["name"]: m["digest"] for m in self.request("/api/tags")["models"]}

    def embed(self, texts):
        started = time.perf_counter()
        result = self.request("/api/embed", {
            "model": self.cfg["embedding_model"], "input": texts,
            "truncate": False, "keep_alive": "5m", "options": {"num_gpu": 0},
        })
        self.calls.append({"stage": "embedding", "seconds": round(time.perf_counter() - started, 3)})
        vectors = np.asarray(result["embeddings"], dtype=np.float32)
        if len(vectors) != len(texts) or not np.isfinite(vectors).all():
            raise ValueError("Embedding inválido")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        if np.any(norms == 0):
            raise ValueError("Embedding nulo")
        return vectors / norms

    def structured(self, prompt_name, data, schema, stage):
        prompt = (BASE / "prompts" / prompt_name).read_text(encoding="utf-8")
        started = time.perf_counter()
        options = dict(self.cfg["generation"])
        if stage != "generation":
            options["num_predict"] = 240
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
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], []
    for sentence in sentences:
        if current and len(" ".join(current + [sentence])) > max_chars:
            chunks.append(" ".join(current))
            current = current[-overlap:] if overlap else []
        current.append(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks


def extract_corpus(cfg):
    from pypdf import PdfReader
    manifest = read_json(BASE / "corpus_manifest.json")
    chunks, source_hashes = [], {}
    for source in manifest["sources"]:
        path = ROOT / source["file"]
        source_hashes[source["id"]] = digest(path.read_bytes())
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
            if len(text) < 80:
                raise ValueError("Trecho insuficiente")
            for i, part in enumerate(split_passage(text, cfg["retrieval"]["chunk_chars"], cfg["retrieval"]["overlap_sentences"])):
                chunks.append({"id": f"{source['id']}-p{passage['printed_page']}-{i + 1}",
                               "source": source["title"], "file": source["file"],
                               "pdf_page": passage["pdf_page"], "printed_page": passage["printed_page"],
                               "text": part})
    return chunks, manifest, source_hashes


def build_index():
    cfg = config()
    chunks, manifest, source_hashes = extract_corpus(cfg)
    client = Ollama(cfg)
    identities = client.identities()
    vectors = client.embed([c["text"] for c in chunks])
    data = BASE / "data"
    data.mkdir(exist_ok=True)
    np.savez_compressed(data / "index.npz", vectors=vectors)
    meta = {"created_at": datetime.now(timezone.utc).isoformat(), "chunks": chunks,
            "embedding_model": cfg["embedding_model"], "embedding_digest": identities[cfg["embedding_model"]],
            "retrieval": cfg["retrieval"], "manifest_hash": digest(manifest), "source_hashes": source_hashes,
            "vector_hash": digest(vectors.tobytes()), "calls": client.calls}
    (data / "chunks.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"chunks": len(chunks), "dimensions": vectors.shape[1], "calls": client.calls}, ensure_ascii=False))


def retrieve(question, cfg, client):
    meta = read_json(BASE / "data" / "chunks.json")
    if meta["manifest_hash"] != digest(read_json(BASE / "corpus_manifest.json")) or meta["retrieval"] != cfg["retrieval"]:
        raise ValueError("Acervo ou parâmetros alterados; reconstrua o índice.")
    if meta["embedding_model"] != cfg["embedding_model"] or meta["embedding_digest"] != client.identities().get(cfg["embedding_model"]):
        raise ValueError("Modelo de embeddings alterado; reconstrua o índice.")
    for source in read_json(BASE / "corpus_manifest.json")["sources"]:
        if digest((ROOT / source["file"]).read_bytes()) != meta["source_hashes"][source["id"]]:
            raise ValueError("PDF alterado; reconstrua o índice.")
    with np.load(BASE / "data" / "index.npz") as index:
        vectors = index["vectors"]
    if digest(vectors.tobytes()) != meta["vector_hash"] or len(vectors) != len(meta["chunks"]):
        raise ValueError("Índice inconsistente")
    scores = vectors @ client.embed([question])[0]
    order = np.argsort(-scores, kind="stable")[:cfg["retrieval"]["top_k"]]
    selected = [dict(meta["chunks"][int(i)], score=round(float(scores[i]), 6)) for i in order
                if scores[i] >= cfg["retrieval"]["min_similarity"]]
    return selected, digest(meta)


def protected_message(action, result):
    return MESSAGES[result.category] if action == "safe_guidance" else MESSAGES["block"]


def save_snapshot(cfg):
    snapshot = {"configuration": cfg, "manifest": read_json(BASE / "corpus_manifest.json"),
                "prompts": {p.name: p.read_text(encoding="utf-8") for p in (BASE / "prompts").glob("*.txt")},
                "implementation": Path(__file__).read_text(encoding="utf-8"),
                "dependencies": (BASE / "requirements-lock.txt").read_text(encoding="utf-8-sig")}
    identifier = digest(snapshot)
    folder = BASE / "runs" / "snapshots"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{identifier}.json"
    if not path.exists():
        path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return identifier


def run_question(question, policy_name=None, case_id=None, group="manual", split="development"):
    if not isinstance(question, str) or not 1 <= len(question.strip()) <= 1500:
        raise ValueError("A pergunta deve conter de 1 a 1500 caracteres.")
    with LOCK:
        return _run(question.strip(), policy_name, case_id, group, split)


def _run(question, policy_name, case_id, group, split):
    cfg = config()
    name = policy_name or cfg["default_policy"]
    if name not in cfg["policies"]:
        raise ValueError("Configuração desconhecida")
    client = Ollama(cfg)
    started = time.perf_counter()
    record = {"id": uuid.uuid4().hex, "time_utc": datetime.now(timezone.utc).isoformat(),
              "question": question, "case_id": case_id, "group": group, "split": split,
              "policy": name, "configuration": cfg, "config_hash": digest(cfg),
              "prompt_hashes": {p.name: digest(p.read_bytes()) for p in (BASE / "prompts").glob("*.txt")},
              "implementation_hash": digest(Path(__file__).read_bytes()),
              "retrieved": [], "input_guard": None, "output_guard": None,
              "generated": None, "valid": False}
    try:
        record["snapshot"] = save_snapshot(cfg)
        record["model_digests"] = client.identities()
        incoming = client.structured("classifier.txt", {"stage": "entrada", "question": question}, Classification, "input_guard")
        action = decision(incoming, cfg["policies"][name])
        record["input_guard"] = dict(incoming.model_dump(), decision=action)
        if action != "allow":
            record.update(action=action, answer=protected_message(action, incoming), final_origin="input_guard")
        else:
            chunks, index_hash = retrieve(question, cfg, client)
            record.update(retrieved=chunks, index_hash=index_hash)
            if not chunks:
                record.update(action="redirect", answer=MESSAGES["redirect"], final_origin="retrieval")
            else:
                generated = client.structured("generator.txt", {"profile": cfg["profile"], "question": question, "sources": chunks}, Generation, "generation")
                record["generated"] = generated.model_dump()
                available = {c["id"] for c in chunks}
                if not generated.supported:
                    record.update(action="redirect", answer=MESSAGES["redirect"], final_origin="model_insufficient_support")
                elif not generated.answer.strip() or not generated.source_ids or not set(generated.source_ids) <= available:
                    raise ValueError("Resposta sem citação válida")
                else:
                    outgoing = client.structured("classifier.txt", {"stage": "saída", "question": question, "answer": generated.answer}, Classification, "output_guard")
                    action = decision(outgoing, cfg["policies"][name])
                    record["output_guard"] = dict(outgoing.model_dump(), decision=action)
                    record.update(action=action, answer=generated.answer if action == "allow" else protected_message(action, outgoing),
                                  final_origin="generation" if action == "allow" else "output_guard")
        record["valid"] = True
    except Exception as exc:
        record.update(action="technical_error", answer=MESSAGES["technical_error"], error=f"{type(exc).__name__}: {exc}", final_origin="technical_error")
    record["seconds"] = round(time.perf_counter() - started, 3)
    record["calls"] = client.calls
    logs = BASE / "runs"
    logs.mkdir(exist_ok=True)
    (logs / f"{record['id']}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["index", "ask"])
    parser.add_argument("question", nargs="?")
    parser.add_argument("--policy", choices=["referencia", "ajustada"], default="ajustada")
    args = parser.parse_args()
    if args.command == "index":
        build_index()
    elif args.question:
        print(json.dumps(run_question(args.question, args.policy), ensure_ascii=False, indent=2))
    else:
        parser.error("Informe a pergunta")


if __name__ == "__main__":
    main()
