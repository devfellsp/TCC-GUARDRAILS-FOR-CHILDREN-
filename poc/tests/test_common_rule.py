import sys
import csv
from collections import Counter
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guardkids as g
import app as web
import evaluation as legacy
import run_development as current
from test_pipeline import classification, environment


def test_comparison_pairs_same_question_channel_and_rule():
    cases = g.read_json(g.BASE / "multichat_cases.json")
    rows = current.schedule(cases)
    assert len(rows) == 32
    assert rows == current.schedule(cases)
    for case in cases:
        pair = [r for r in rows if r["case_id"] == case["id"]]
        assert len(pair) == 2 and {r["response_style"] for r in pair} == set(g.RESPONSE_STYLES)
        assert all(r["question"] == case["question"] and r["channel"] == case["channel"]
                   and r["policy"] == "comum" for r in pair)
    assert Counter(rows[i]["response_style"] for i in range(0, len(rows), 2)) == {"padrao":8, "passo_a_passo":8}


def test_old_rules_cannot_be_selected_in_api(monkeypatch):
    def unexpected(*args, **kwargs):
        raise AssertionError("Regras antigas não devem chegar à inferência")
    monkeypatch.setattr(web, "run_question", unexpected)
    client = TestClient(web.app, base_url="http://127.0.0.1:8765")
    for policy in ["ajustada", "referencia"]:
        assert client.post("/api/ask", json={"question":"Teste", "policy":policy}).status_code == 422


@pytest.mark.parametrize("channel", list(g.CHANNELS))
@pytest.mark.parametrize("style", list(g.RESPONSE_STYLES))
def test_common_rule_accepts_educational_predation_but_blocks_harm(environment, monkeypatch, channel, style):
    educational = classification(educational_predation=True)
    replies = iter([educational, g.Generation(supported=True, answer="Explicação fictícia com fonte.", source_ids=["c1"]),
                    g.Grounding(supported=True, reason="Teste"), educational,
                    classification(category="danger", needs_protection=True, educational_predation=True)])
    monkeypatch.setattr(g.Ollama, "structured", lambda *args: next(replies))
    allowed = g.run_question("Caso educativo fictício", channel=channel, response_style=style)
    blocked = g.run_question("Caso prejudicial fictício", channel=channel, response_style=style)
    assert allowed["valid"] and allowed["action"] == "allow"
    assert blocked["valid"] and blocked["action"] == "block" and blocked["generated"] is None
    for record in [allowed, blocked]:
        assert record["channel"] == channel and record["response_style"] == style and record["policy"] == "comum"


@pytest.mark.parametrize("operation", [legacy.freeze, legacy.verify_freeze, legacy.calibration])
def test_archived_protocol_cannot_run_under_current_rule(operation):
    with pytest.raises(ValueError, match="arquivado"):
        operation()


def test_new_config_cannot_restore_conservative_rule():
    cfg = g.config()
    cfg["policies"]["comum"]["allow_educational_predation"] = False
    with pytest.raises(ValueError, match="regra comum"):
        g.Settings.model_validate(cfg)


def test_runner_preserves_loss_and_review_fields_without_retry(tmp_path, monkeypatch):
    agenda = current.schedule([{"id":"one", "group":"legitima", "question":"Caso fictício", "expected":"allow"}])
    monkeypatch.setattr(current, "save_snapshot", lambda cfg:"fixed")
    calls = []
    def fake(*args, **kwargs):
        calls.append(kwargs["response_style"])
        ok = len(calls) > 1
        return {"action":"allow" if ok else "technical_error", "valid":ok, "seconds":1,
                "answer":"Resposta" if ok else "Erro", "id":str(len(calls)), "snapshot":"fixed"}
    monkeypatch.setattr(current, "run_question", fake)
    current.execute(agenda, tmp_path, "multichat")
    with (tmp_path / "resultados.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(calls) == len(rows) == 2
    assert rows[0]["valid"] == "False" and rows[0]["human_safety"] == ""
    assert rows[1]["valid"] == "True" and rows[1]["human_source_support"] == ""
    assert g.read_json(tmp_path / "resumo.json")["technical_losses"] == 1
