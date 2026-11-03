import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guardkids as g


def classification(**kwargs):
    return g.Classification(category="normal", needs_protection=False, educational_predation=False, reason="teste").model_copy(update=kwargs)


def test_context_exception_does_not_allow_harm():
    harmful = classification(category="danger", needs_protection=True, educational_predation=True)
    assert g.decision(harmful, {"allow_educational_predation": True}) == "block"
    educational = classification(educational_predation=True)
    assert g.decision(educational, {"allow_educational_predation": True}) == "allow"
    assert g.decision(educational, {"allow_educational_predation": False}) == "block"


@pytest.fixture
def environment(monkeypatch, tmp_path):
    cfg = g.config()
    prompts = tmp_path / "prompts"
    prompts.mkdir()
    (prompts / "generator.txt").write_text("test")
    monkeypatch.setattr(g, "BASE", tmp_path)
    monkeypatch.setattr(g, "config", lambda: cfg)
    monkeypatch.setattr(g, "save_snapshot", lambda cfg: "snapshot-test")
    monkeypatch.setattr(g.Ollama, "identities", lambda self: {"qwen3:8b": "test"})
    monkeypatch.setattr(g, "retrieve", lambda *args: ([{"id": "c1", "text": "Fonte"}], "hash"))
    return tmp_path


def test_output_protection_replaces_generated_content(environment, monkeypatch):
    responses = iter([classification(), g.Generation(supported=True, answer="CONTEUDO_REJEITADO", source_ids=["c1"]), classification(category="danger", needs_protection=True)])
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: next(responses))
    result = g.run_question("Pergunta fictícia")
    assert result["valid"] and result["final_origin"] == "output_guard"
    assert "CONTEUDO_REJEITADO" not in result["answer"]
    assert result["generated"]["answer"] == "CONTEUDO_REJEITADO"
    assert len(list((environment / "runs").glob("*.json"))) == 1


def test_model_failure_is_technical_loss(environment, monkeypatch):
    def fail(*args):
        raise TimeoutError("timeout")
    monkeypatch.setattr(g.Ollama, "structured", fail)
    result = g.run_question("Pergunta fictícia")
    assert result["valid"] is False
    assert result["action"] == "technical_error"
    assert result["input_guard"] is None


def test_unknown_source_is_not_displayed(environment, monkeypatch):
    responses = iter([classification(), g.Generation(supported=True, answer="Resposta", source_ids=["inventada"])])
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: next(responses))
    result = g.run_question("Pergunta fictícia")
    assert not result["valid"]
    assert result["answer"] != "Resposta"


def test_input_block_skips_retrieval(environment, monkeypatch):
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: classification(category="privacy", needs_protection=True))
    def unexpected(*args):
        raise AssertionError("Recuperação não deveria ocorrer")
    monkeypatch.setattr(g, "retrieve", unexpected)
    result = g.run_question("Meu endereço é ...")
    assert result["valid"] and result["action"] == "safe_guidance"
    assert not result["retrieved"] and result["generated"] is None


def test_configs_differ_in_exactly_one_policy_parameter():
    cfg = g.config()
    before = cfg["policies"]["referencia"]
    after = cfg["policies"]["ajustada"]
    assert set(before) == set(after)
    assert [key for key in before if before[key] != after[key]] == ["allow_educational_predation"]


def test_browser_api_never_returns_rejected_draft(monkeypatch):
    from fastapi.testclient import TestClient
    import app
    monkeypatch.setattr(app, "run_question", lambda *args: {
        "id": "test", "answer": "Mensagem segura", "action": "block", "valid": True,
        "seconds": 1.0, "policy": "ajustada", "generated": {"answer": "REJEITADO", "source_ids": ["c1"]},
        "retrieved": [{"id": "c1", "text": "NAO_ENVIAR"}], "calls": [],
    })
    client = TestClient(app.app)
    response = client.post("/api/ask", json={"question": "Pergunta fictícia"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Mensagem segura"
    assert response.json()["sources"] == []
    assert "REJEITADO" not in response.text and "NAO_ENVIAR" not in response.text


def test_empty_retrieval_redirects_without_generation(environment, monkeypatch):
    monkeypatch.setattr(g, "retrieve", lambda *args: ([], "hash"))
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: classification())
    result = g.run_question("Pergunta sem trecho suficiente")
    assert result["valid"] and result["action"] == "redirect"
    assert result["generated"] is None
