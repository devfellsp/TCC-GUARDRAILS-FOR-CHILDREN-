import copy
import json
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guardkids as g
import app as web
from privacy import OMITTED
from settings import Settings
from test_pipeline import classification, environment


@pytest.fixture(scope="module")
def corpus():
    cfg = g.config()
    chunks, manifest, hashes = g.extract_corpus(cfg)
    return cfg, chunks, manifest, hashes


@pytest.fixture
def index_environment(monkeypatch, tmp_path, corpus):
    cfg, chunks, manifest, hashes = copy.deepcopy(corpus)
    (tmp_path / "corpus_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(g, "BASE", tmp_path)
    monkeypatch.setattr(g, "config", lambda: cfg)
    vectors = np.zeros((len(chunks), 4), dtype=np.float32)
    vectors[:, 0] = 1
    meta = {"chunks": chunks, "embedding_model": cfg["embedding_model"], "embedding_digest": "test",
            "retrieval": cfg["retrieval"], "manifest_hash": g.digest(manifest), "source_hashes": hashes,
            "vector_hash": g.digest(vectors.tobytes())}
    identifier = g.publish_index(meta, vectors)
    return cfg, meta, vectors, identifier, tmp_path


def test_real_corpus_extraction_has_auditable_anchors(corpus):
    cfg, chunks, _, _ = corpus
    assert len([c for c in chunks if c["channel"] == "ciencias"]) == 5
    assert len({c["id"] for c in chunks}) == len(chunks)
    assert {c["channel"] for c in chunks} == {"ciencias", "historia", "geografia", "geral"}
    assert all(80 <= len(c["text"]) <= cfg["retrieval"]["chunk_chars"] for c in chunks)
    source = next(c["text"] for c in chunks if c["id"] == "sp2024-p9-1")
    assert "açúcar" in source and "folhas" in source


@pytest.mark.parametrize("text", ["a" * 900 + ". " + "b" * 900, "Uma frase curta. " * 50])
def test_split_preserves_content_and_enforces_hard_limit(text):
    chunks = g.split_passage(text, 850, 1)
    assert chunks and all(0 < len(c) <= 850 for c in chunks)
    assert all(chunk in g.clean(text) for chunk in chunks)


def test_index_roundtrip_and_retrieval(index_environment, monkeypatch):
    cfg, meta, vectors, identifier, _ = index_environment
    client = g.Ollama(cfg)
    monkeypatch.setattr(client, "identities", lambda: {cfg["embedding_model"]: "test"})
    monkeypatch.setattr(client, "embed", lambda _: vectors[:1])
    selected, actual = g.retrieve("Pergunta ficticia", cfg, client)
    assert actual == identifier and len(selected) == cfg["retrieval"]["top_k"]
    assert selected[0]["id"] == meta["chunks"][0]["id"]


def test_metadata_tampering_rejected_even_if_pointer_recalculated(index_environment):
    cfg, meta, vectors, _, folder = index_environment
    meta["chunks"][0]["text"] = "Texto adulterado"
    g.publish_index(meta, vectors)
    with pytest.raises(ValueError, match="divergem"):
        g.load_index(cfg)


def test_corrupted_vector_rejected(index_environment):
    cfg, meta, vectors, identifier, folder = index_environment
    vectors[0] *= 2
    np.savez_compressed(folder / "data/indices" / identifier / "index.npz", vectors=vectors)
    with pytest.raises(ValueError, match="inconsistente"):
        g.load_index(cfg)
    with pytest.raises(ValueError, match="alterada"):
        g.publish_index(meta, vectors)


def test_model_change_requires_reindex(index_environment):
    cfg, _, _, _, _ = index_environment
    with pytest.raises(ValueError, match="embeddings"):
        g.load_index(cfg, {cfg["embedding_model"]: "changed"})


def test_status_fails_closed_without_metadata(monkeypatch, tmp_path):
    cfg = g.config()
    monkeypatch.setattr(g, "BASE", tmp_path)
    monkeypatch.setattr(web, "config", lambda: cfg)
    monkeypatch.setattr(web.Ollama, "identities", lambda self: {cfg["model"]: "a", cfg["embedding_model"]: "b"})
    (tmp_path / "data").mkdir()
    (tmp_path / "data/index.npz").write_bytes(b"broken")
    assert web.status()["ready"] is False


def test_status_accepts_only_valid_current_index(index_environment, monkeypatch):
    cfg, _, _, _, _ = index_environment
    monkeypatch.setattr(web, "config", lambda: cfg)
    monkeypatch.setattr(web.Ollama, "identities", lambda self: {cfg["model"]: "a", cfg["embedding_model"]: "test"})
    assert web.status()["ready"] is True


def test_private_input_is_not_sent_to_model_or_saved(environment, monkeypatch):
    def unexpected(*args):
        raise AssertionError("Nao deve chamar o modelo")
    monkeypatch.setattr(g.Ollama, "structured", unexpected)
    result = g.run_question("Meu contato ficticio e revisao@example.invalid")
    assert result["valid"] and result["action"] == "safe_guidance"
    text = next((environment / "runs").glob("*.json")).read_text(encoding="utf-8")
    assert "revisao@example.invalid" not in text
    assert json.loads(text)["question"] == OMITTED


def test_unrecognized_free_text_is_also_omitted_from_logs(environment, monkeypatch):
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: classification(category="privacy", needs_protection=True, reason="IDENTIFICADOR_SEM_REGEX"))
    result = g.run_question("IDENTIFICADOR_SEM_REGEX")
    text = (environment / "runs" / f"{result['id']}.json").read_text(encoding="utf-8")
    assert "IDENTIFICADOR_SEM_REGEX" not in text


def test_synthetic_logging_requires_explicit_call(environment, monkeypatch):
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: classification(needs_protection=True, category="danger"))
    result = g.run_question("CASO_FICTICIO", synthetic=True)
    saved = g.read_json(environment / "runs" / f"{result['id']}.json")
    assert saved["question"] == "CASO_FICTICIO" and saved["logging_mode"] == "synthetic"


def test_generation_and_grounding_success(environment, monkeypatch):
    responses = iter([classification(), g.Generation(supported=True, answer="Resposta apoiada", source_ids=["c1"]),
                      g.Grounding(supported=True, reason="Fonte sustenta"), classification()])
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: next(responses))
    result = g.run_question("Pergunta ficticia")
    assert result["valid"] and result["action"] == "allow"
    saved = g.read_json(environment / "runs" / f"{result['id']}.json")
    assert saved["answer"] == OMITTED and saved["generated"]["answer"] == OMITTED


@pytest.mark.parametrize("generator_supported", [False, True])
def test_unsupported_generation_is_redirected(environment, monkeypatch, generator_supported):
    responses = iter([classification(), g.Generation(supported=generator_supported, answer="Afirmação sem apoio", source_ids=["c1"]),
                      g.Grounding(supported=False, reason="Nao consta na fonte")])
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: next(responses))
    result = g.run_question("Pergunta ficticia")
    assert result["valid"] and result["action"] == "redirect" and result["output_guard"] is None


def test_answer_word_limit_is_enforced(environment, monkeypatch):
    responses = iter([classification(), g.Generation(supported=True, answer="palavra " * 121, source_ids=["c1"])])
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: next(responses))
    result = g.run_question("Pergunta ficticia")
    assert not result["valid"] and result["action"] == "technical_error"


def test_busy_request_is_rejected_without_waiting():
    assert g.LOCK.acquire(blocking=False)
    try:
        with pytest.raises(g.BusyError):
            g.run_question("Pergunta ficticia")
    finally:
        g.LOCK.release()


def test_expired_or_cancelled_request_cannot_release_answer(environment, monkeypatch):
    cancelled = threading.Event()
    cancelled.set()
    result = g.run_question("Meu email e teste@example.invalid", cancelled=cancelled)
    assert not result["valid"] and result["action"] == "technical_error"
    client = g.Ollama(g.config(), deadline=time.monotonic() - 1)
    with pytest.raises(TimeoutError):
        client.check_budget()


def test_disk_failure_withholds_response_and_releases_lock(environment, monkeypatch):
    monkeypatch.setattr(g, "atomic_json", lambda *args: (_ for _ in ()).throw(OSError("disk full")))
    with pytest.raises(g.PersistenceError):
        g.run_question("Meu email e teste@example.invalid")
    assert not g.LOCK.locked()


def test_config_rejects_remote_model_and_invalid_limits():
    cfg = g.config()
    cfg["ollama_url"] = "http://exemplo.invalid:11434"
    with pytest.raises(ValidationError):
        Settings.model_validate(cfg)
    cfg = g.config()
    cfg["retrieval"]["top_k"] = 0
    with pytest.raises(ValidationError):
        Settings.model_validate(cfg)


def test_log_expiry_preserves_legacy_and_research(environment):
    logs = environment / "runs"
    logs.mkdir()
    old = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
    for mode in ["minimized", "synthetic", "legacy"]:
        (logs / f"{mode}.json").write_text(json.dumps({"logging_mode": mode, "time_utc": old}))
    assert g.prune_logs()["files"] == ["minimized.json"]
    assert (logs / "minimized.json").exists()
    g.prune_logs(apply=True)
    assert not (logs / "minimized.json").exists()
    assert (logs / "synthetic.json").exists() and (logs / "legacy.json").exists()


@pytest.fixture
def api_client():
    from fastapi.testclient import TestClient
    return TestClient(web.app, base_url="http://127.0.0.1:8765")


def test_api_rejects_untrusted_hosts_origins_and_large_body(api_client):
    assert api_client.get("/", headers={"Host": "nao-autorizado.invalid"}).status_code == 400
    assert api_client.post("/api/ask", json={"question": "Teste"}, headers={"Origin": "http://nao-autorizado.invalid"}).status_code == 403
    assert api_client.post("/api/ask", content="x" * 8193).status_code == 413
    assert api_client.post("/api/ask", content='{"question":"Teste"}').status_code == 422
    assert api_client.post("/api/ask", json={"question": "Teste", "synthetic": True}).status_code == 422
    assert api_client.post("/api/ask", json={"question": "Teste", "policy": "unknown"}).status_code == 422


def test_api_reports_busy_and_persistence_failure(api_client, monkeypatch):
    for error, status in [(g.BusyError("Ocupado"), 429), (g.PersistenceError("Disco"), 503)]:
        def fail(*args, **kwargs):
            raise error
        monkeypatch.setattr(web, "run_question", fail)
        assert api_client.post("/api/ask", json={"question": "Teste"}).status_code == status
    assert api_client.get("/api/health").json() == {"alive": True}


def test_snapshot_contains_replayable_index_and_runtime(index_environment):
    cfg, _, vectors, identifier, folder = index_environment
    (folder / "prompts").mkdir()
    (folder / "requirements-lock.txt").write_text("pypdf==6.21.4")
    (folder / "app.py").write_text("# teste")
    snapshot_id = g.save_snapshot(cfg)
    snapshot = g.read_json(folder / "runs/snapshots" / f"{snapshot_id}.json")
    assert snapshot["index"]["id"] == identifier
    assert np.array_equal(np.asarray(snapshot["index"]["vectors"], dtype=np.float32), vectors)
    assert "app.py" in snapshot["implementation"]
    assert "python" in snapshot["runtime"] and "pypdf" in snapshot["runtime"]["packages"]
