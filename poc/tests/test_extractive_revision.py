"""Regressões reais da barreira adicional da GK-P2.5-dev."""
import csv
import importlib.util
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
VERSION = ROOT / "poc/versions/GK-P2.5-dev"
OLD = ROOT / "avaliacao/evidencias/ampliacao_GK_P2_2_dev_20261105"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, VERSION / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


dependencies = ("channels", "response_styles", "privacy", "settings", "vocabulary")
previous = {name: sys.modules.get(name) for name in dependencies}
try:
    for name in dependencies: load(name, name + ".py")
    g = load("guardkids_final", "guardkids.py")
    privacy = sys.modules["privacy"]
finally:
    for name, module in previous.items():
        if module is None: sys.modules.pop(name, None)
        else: sys.modules[name] = module


@pytest.mark.parametrize("case,style,allowed", [
    ("exp22-g04", "padrao", False), ("exp22-g04", "passo_a_passo", False),
    ("exp22-h04", "passo_a_passo", False), ("exp22-h02", "passo_a_passo", False),
    ("exp22-h04", "padrao", True), ("exp22-h05", "padrao", True)])
def test_known_unanchored_details_are_withheld_without_rejecting_supported_controls(case, style, allowed):
    with (OLD / "resultados.csv").open(encoding="utf-8-sig", newline="") as stream:
        row = next(r for r in csv.DictReader(stream) if r["case_id"] == case and r["response_style"] == style)
    raw = g.read_json(OLD / "runs" / f"{row['run_id']}.json")
    draft = g.Draft(supported=True, claims=[g.Claim(text=raw["answer"], evidence=[g.Evidence(source_id=identifier)
                         for identifier in raw["generated"]["source_ids"]])])
    assert (g.assemble_draft(draft, raw["retrieved"], "padrao") is not None) == allowed


def test_quote_text_comes_from_retrieval_and_cannot_be_supplied_by_generator():
    source = dict(id="fonte", text="A soja é utilizada para a produção do óleo de cozinha.")
    draft = g.Draft(supported=True, claims=[g.Claim(text="A soja é utilizada para a produção do óleo de cozinha.",
                    evidence=[g.Evidence(source_id="fonte")])])
    assert g.claim_evidence(draft, [source])[0]["evidence"][0]["quote"] == source["text"]
    assert g.assemble_draft(draft, [source], "padrao")
    with pytest.raises(ValueError):
        g.Evidence.model_validate(dict(source_id="fonte", quote="Citação inventada"))


def test_unanchored_numbers_are_not_allowed():
    source = dict(id="fonte", text="A agricultura contribuiu para o estoque de produtos.")
    draft = g.Draft(supported=True, claims=[g.Claim(text="A agricultura contribuiu para 500 produtos.",
                    evidence=[g.Evidence(source_id="fonte")])])
    assert g.assemble_draft(draft, [source], "padrao") is None


def test_new_provenance_is_omitted_from_private_logs():
    record = dict(question="Pergunta privada", answer="Resposta privada", final_origin="generation",
                  claim_evidence=[dict(text="Texto privado", evidence=[])])
    assert privacy.log_record(record)["claim_evidence"] == privacy.OMITTED


@pytest.mark.parametrize("accepted", [True, False])
def test_literal_alternative_keeps_original_failure_and_must_pass_audit(tmp_path, monkeypatch, accepted):
    cfg = g.config()
    monkeypatch.setattr(g, "BASE", tmp_path)
    monkeypatch.setattr(g, "config", lambda: cfg)
    monkeypatch.setattr(g, "save_snapshot", lambda cfg: "snapshot-ficticio")
    source = dict(id="fonte", text="As migrações contribuem para uma cultura rica e diversificada.")
    monkeypatch.setattr(g, "retrieve", lambda *a: ([source], "indice-ficticio"))
    calls = []
    class Client:
        def __init__(self, *a, **kw): self.calls = []
        def identities(self): return {}
        def request(self, endpoint): return {"version": "simulada"}
        def check_budget(self): pass
        def structured(self, prompt, data, schema, stage):
            calls.append(stage)
            if stage in {"input_guard", "output_guard"}:
                return g.Classification(category="normal", needs_protection=False, educational_predation=False,
                                        help_seeking=False, reason="Cenário simulado")
            if stage == "generation":
                return g.Draft(supported=True, claims=[g.Claim(text="As migrações trazem música e idiomas.",
                                evidence=[g.Evidence(source_id="fonte")])])
            assert data["answer"] == source["text"]
            return g.Grounding(claims=[g.ClaimVerdict(claim=1, supported=accepted, reason="Cenário simulado")],
                               answers_question=accepted, language_ok=True, reason="Cenário simulado")
    monkeypatch.setattr(g, "Ollama", Client)
    result = g.run_question("Como a migração contribui para a cultura?", synthetic=True, channel="geografia")
    assert result["valid"] and result["action"] == ("allow" if accepted else "redirect")
    assert result["candidate_checks"][0]["rejected_by"] == "evidence_guard"
    assert "música" in result["draft"]["claims"][0]["text"]
    assert "música" not in result["answer"] and calls.count("generation") == 1
    if accepted:
        assert result["answer"] == source["text"] and result["final_origin"] == "extractive_fallback"
        saved = privacy.log_record(result)
        assert saved["answer"] == saved["released_draft"] == saved["candidate_checks"] == privacy.OMITTED
    else:
        assert result["answer"] == g.MESSAGES["redirect"]


def test_literal_alternative_copies_only_existing_sentences_within_limits():
    source = dict(id="fonte", text="A agricultura trouxe estoques. Os estoques contribuíram para as trocas.")
    proposal = g.extractive_draft([source])
    assert len(proposal.claims) == 2
    for claim in proposal.claims:
        assert claim.text in source["text"]
    assert g.assemble_draft(proposal, [source], "passo_a_passo")
    assert g.extractive_draft([dict(id="longo", text="a " * 300)]) is None


