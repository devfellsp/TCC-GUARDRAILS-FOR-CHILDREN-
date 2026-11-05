import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guardkids as g
import app as web
from test_pipeline import environment, classification
from test_hardening import corpus, index_environment


def test_retrieval_filters_before_top_k(index_environment, monkeypatch):
    cfg, meta, vectors, identifier, _ = index_environment
    client = g.Ollama(cfg)
    monkeypatch.setattr(client, "identities", lambda: {cfg["embedding_model"]: "test"})
    monkeypatch.setattr(client, "embed", lambda _: vectors[:1])
    for channel in g.CHANNELS:
        selected, _ = g.retrieve("Pergunta fictícia", cfg, client, channel)
        assert selected and all(c["channel"] == channel for c in selected)


def test_api_validates_and_forwards_channel(monkeypatch):
    observed = []
    def fake(question, policy, **kwargs):
        observed.append(kwargs["channel"])
        return {"id":"test", "answer":"Seguro", "action":"redirect", "valid":True,
                "seconds":0.1, "policy":"comum", "channel":kwargs["channel"],
                "retrieved":[], "calls":[]}
    monkeypatch.setattr(web, "run_question", fake)
    with TestClient(web.app, base_url="http://127.0.0.1:8765") as client:
        assert set(client.get("/api/channels").json()) == set(g.CHANNELS)
        for channel in g.CHANNELS:
            response = client.post("/api/ask", json={"question":"Caso fictício", "channel":channel})
            assert response.status_code == 200 and response.json()["channel"] == channel
        assert client.post("/api/ask", json={"question":"Caso fictício", "channel":"inventado"}).status_code == 422
    assert observed == list(g.CHANNELS)


def test_channel_scope_reaches_generator_and_record(environment, monkeypatch):
    responses = iter([classification(), g.Generation(supported=False, answer="", source_ids=[])])
    payloads = []
    def structured(self, prompt, data, *args):
        payloads.append((prompt, data))
        return next(responses)
    monkeypatch.setattr(g.Ollama, "structured", structured)
    result = g.run_question("O que são fontes históricas?", channel="historia", synthetic=True, response_style="passo_a_passo")
    assert result["valid"] and result["channel"] == "historia"
    assert payloads[1][1]["scope"] == g.CHANNELS["historia"]["scope"]
    assert payloads[1][1]["response_style"] == result["response_style"] == "passo_a_passo"
    assert result["action"] == "redirect"


def test_unknown_channel_rejected_before_run():
    with pytest.raises(ValueError, match="Chat desconhecido"):
        g.run_question("Caso fictício", channel="inventado")
