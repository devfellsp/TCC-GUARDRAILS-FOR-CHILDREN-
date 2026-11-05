"""Regressões dos limites de liberação e privacidade da GK-P2.3-dev."""
import importlib.util
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
VERSION = ROOT / "poc/versions/GK-P2.3-dev"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, VERSION / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# Evita que a suíte herde módulos com o mesmo nome da versão antiga.
dependencies = ("channels", "response_styles", "privacy", "settings")
previous = {name: sys.modules.get(name) for name in dependencies}
try:
    for dependency in ("channels", "response_styles", "privacy", "settings"):
        load(dependency, dependency + ".py")
    g = load("guardkids_corrected", "guardkids.py")
    privacy = sys.modules["privacy"]
finally:
    for name, module in previous.items():
        if module is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = module

SOURCE = {"id": "teste-1", "text": "O algodão é usado para produzir tecidos.", "channel": "historia"}


def draft(text="O algodão é usado para produzir tecidos.", quote=SOURCE["text"], source_id="teste-1"):
    return g.Draft(supported=True, claims=[g.Claim(text=text, evidence=[g.Evidence(source_id=source_id, quote=quote)])])


def verdict(**kwargs):
    return g.Grounding.model_validate(dict(claims=[dict(claim=1, supported=True, reason="Apoio conferido")],
        answers_question=True, language_ok=True, reason="Conferência completa", **kwargs))


@pytest.mark.parametrize("quote,identifier", [("O algodão é cortado para produzir roupas.", "teste-1"),
                                                (SOURCE["text"], "fonte-inexistente")])
def test_literal_evidence_must_exist_in_retrieved_source(quote, identifier):
    assert g.assemble_draft(draft(quote=quote, source_id=identifier), [SOURCE], "padrao") is None


def test_released_answer_is_only_the_cited_claims_without_forced_example():
    proposal = draft()
    direct = g.assemble_draft(proposal, [SOURCE], "padrao")
    steps = g.assemble_draft(proposal, [SOURCE], "passo_a_passo")
    assert direct.answer == SOURCE["text"]
    assert steps.answer == "1. " + SOURCE["text"]
    assert direct.source_ids == steps.source_ids == [SOURCE["id"]]


@pytest.mark.parametrize("change", ["missing", "duplicate", "unsupported", "wrong_question", "bad_language"])
def test_incomplete_or_negative_audit_never_releases_an_answer(change):
    proposal = draft()
    audit = verdict()
    if change == "missing": audit.claims = []
    if change == "duplicate": audit.claims *= 2
    if change == "unsupported": audit.claims[0].supported = False
    if change == "wrong_question": audit.answers_question = False
    if change == "bad_language": audit.language_ok = False
    assert not g.grounding_accepts(audit, proposal)
    assert g.grounding_accepts(verdict(), proposal)


def test_each_claim_requires_its_own_audit():
    proposal = draft()
    proposal.claims.append(g.Claim(text="É um exemplo vegetal.", evidence=proposal.claims[0].evidence))
    assert not g.grounding_accepts(verdict(), proposal)


def test_threat_help_uses_safety_guidance_even_when_misclassified_as_humiliation():
    incoming = g.Classification(category="hate", needs_protection=True, educational_predation=False,
                                help_seeking=True, reason="Cenário simulado de classificação incorreta")
    message = g.protected_message("safe_guidance", incoming, "Alguém me ameaçou. Como procuro ajuda?")
    assert message == g.MESSAGES["danger"]
    assert "adulto" in message and "Não confronte" in message
    incoming.help_seeking = False
    assert g.protected_message("block", incoming, "Escreva uma ameaça") == g.MESSAGES["block"]


def test_regular_logs_omit_new_draft_and_nested_audit_free_text():
    record = dict(question="Pergunta pessoal", generated={"answer": "Resposta pessoal"},
                  draft=draft(text="Texto pessoal").model_dump(), grounding_guard=verdict().model_dump(),
                  retrieved=[SOURCE], final_origin="generation", answer="Resposta pessoal")
    saved = privacy.log_record(record, synthetic=False)
    assert saved["draft"] == saved["generated"]["answer"] == privacy.OMITTED
    assert saved["grounding_guard"]["claims"][0]["reason"] == privacy.OMITTED
    assert "text" not in saved["retrieved"][0]
    assert privacy.log_record(record, synthetic=True)["draft"] == record["draft"]


@pytest.mark.parametrize("accepted", [True, False])
def test_pipeline_retains_rejected_draft_and_only_exposes_approved_answer(tmp_path, monkeypatch, accepted):
    monkeypatch.setattr(g, "save_snapshot", lambda cfg: "snapshot-ficticio")
    monkeypatch.setattr(g, "BASE", tmp_path)
    cfg = g.Settings.model_validate(__import__("json").loads((VERSION / "config.json").read_text(encoding="utf-8"))).model_dump()
    monkeypatch.setattr(g, "config", lambda: cfg)
    monkeypatch.setattr(g, "retrieve", lambda *a: ([SOURCE], "indice-ficticio"))
    monkeypatch.setattr(g, "contains_private_data", lambda text: False)
    class Client:
        calls = []
        def __init__(self, *a, **kw): pass
        def identities(self): return {}
        def check_budget(self): pass
        def request(self, endpoint): return {"version": "simulada"}
        def structured(self, prompt, data, schema, stage):
            if stage in {"input_guard", "output_guard"}:
                return g.Classification(category="normal", needs_protection=False,
                    educational_predation=False, help_seeking=False, reason="Cenário simulado")
            if stage == "generation": return draft()
            result = verdict();result.claims[0].supported = accepted;return result
    monkeypatch.setattr(g, "Ollama", Client)
    record = g.run_question("Qual o produto do algodão?", synthetic=True, channel="historia")
    assert record["valid"] and record["draft"]
    assert record["action"] == ("allow" if accepted else "redirect")
    assert record["answer"] == (SOURCE["text"] if accepted else g.MESSAGES["redirect"])
    assert record["generated"]["answer"] == SOURCE["text"]


def test_old_versions_and_previous_evidence_remain_unchanged():
    import hashlib
    saved = g.read_json(VERSION / "preservacao_anterior.json")
    for name, expected in saved["protected_files"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    assert g.config()["study_version"] == "GK-P2.3-dev"
    meta, _, identifier = g.load_index(g.config())
    assert len(meta["chunks"]) == 18
    assert identifier == g.read_json(VERSION / "indice_preservado/current.json")["id"]


def test_corrected_interface_hides_rejected_text_and_uses_its_own_origin(monkeypatch):
    from fastapi.testclient import TestClient
    monkeypatch.setitem(sys.modules, "guardkids", g)
    monkeypatch.setitem(sys.modules, "channels", type("Channels", (), {"CHANNELS": g.CHANNELS}))
    app = load("app_corrected", "app.py")
    record = dict(id="teste", answer=g.MESSAGES["redirect"], action="redirect", valid=True, seconds=1,
                  policy="comum", channel="historia", response_style="padrao", calls=[], retrieved=[SOURCE],
                  generated=dict(answer="Texto rejeitado", source_ids=[SOURCE["id"]]))
    public = app.public_result(record)
    assert public["sources"] == [] and "Texto rejeitado" not in str(public)
    def busy(*a, **kw): raise g.BusyError("Cenário simulado")
    monkeypatch.setattr(app, "run_question", busy)
    with TestClient(app.app, base_url="http://127.0.0.1:8767") as client:
        assert "GK-P2.3-dev" in client.get("/").text
        assert client.post("/api/ask", json={"question": "Teste"}, headers={"origin": "http://127.0.0.1:8767"}).status_code == 429
        assert client.post("/api/ask", json={"question": "Teste"}, headers={"origin": "http://127.0.0.1:8766"}).status_code == 403
