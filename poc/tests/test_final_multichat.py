import csv
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guardkids as g
import final_multichat as f


def test_reserved_plan_balances_styles_families_and_second_review():
    cases, protocol = f.inputs()
    rows = f.schedule(cases, protocol["seed"])
    assert len(rows) == 64 and len({r["observation_id"] for r in rows}) == 64
    assert rows == f.schedule(cases, protocol["seed"])
    assert Counter(r["response_style"] for r in rows) == {"padrao":32, "passo_a_passo":32}
    selected = [r for r in rows if r["secondary_review"]]
    assert len(selected) == 16 and len({r["family_id"] for r in selected}) == 16
    assert set(Counter(r["channel"] for r in selected).values()) == {4}
    assert Counter(r["response_style"] for r in selected) == {"padrao":8, "passo_a_passo":8}
    for field in ("channel", "group"):
        for value in {r[field] for r in selected}:
            assert Counter(r["response_style"] for r in selected if r[field] == value) == {
                "padrao": 2, "passo_a_passo": 2}
    reversed_selection = {r["observation_id"] for r in f.schedule(list(reversed(cases)), protocol["seed"])
                          if r["secondary_review"]}
    assert reversed_selection == {r["observation_id"] for r in selected}
    for case in cases:
        pair = [r for r in rows if r["case_id"] == case["id"]]
        assert len(pair) == 2 and {r["response_style"] for r in pair} == set(g.RESPONSE_STYLES)


def test_reserved_cases_have_references_and_no_literal_development_reuse():
    cases, _ = f.inputs()
    development = {c["question"] for c in g.read_json(g.BASE / "multichat_cases.json")}
    chunks, _, _ = g.extract_corpus(g.config())
    for case in cases:
        assert case["question"] not in development
        assert case["human_reference_status"] == "pendente"
        for identifier in case["reference_ids"]:
            assert any(c["id"] == identifier and c["channel"] == case["channel"] for c in chunks)


def test_prospective_review_forms_match_corrected_agenda_and_remain_blank():
    cases, protocol = f.inputs()
    agenda = f.schedule(cases, protocol["seed"])
    assert g.read_json(f.STUDY / "agenda_planejada.json") == agenda
    selected = {r["observation_id"] for r in agenda if r["secondary_review"]}
    for filename in ("parecer_secundario.csv", "conciliacao.csv"):
        with (f.STUDY / filename).open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == 16
        assert {r["review_id"] for r in rows} == selected
        assert all(not v for r in rows for k, v in r.items() if k not in {"review_id", "papel"})
    with (f.STUDY / "comparacao_clareza.csv").open(encoding="utf-8-sig", newline="") as stream:
        pairs = list(csv.DictReader(stream))
    assert len(pairs) == 32 and len({p["case_id"] for p in pairs}) == 32
    for pair in pairs:
        expected = {r["observation_id"] for r in agenda if r["case_id"] == pair["case_id"]}
        assert {pair["review_id_a"], pair["review_id_b"]} == expected
        assert all(not pair[k] for k in ("preferencia", "avaliador", "data", "justificativa"))


def test_incomplete_human_reference_rejected_without_signature():
    with pytest.raises(ValueError, match="incompleta"):
        f.ratify(f.STUDY / "referencia_humana.csv")
    assert not (f.STUDY / "referencia_ratificada.json").exists()


def test_final_run_requires_human_reference_before_network_or_output(monkeypatch, tmp_path):
    monkeypatch.setattr(f, "STUDY", tmp_path)
    def unexpected(*args, **kwargs):
        raise AssertionError("Não pode chamar o modelo")
    monkeypatch.setattr(g, "Ollama", unexpected)
    with pytest.raises(ValueError, match="ratificação humana pendente"):
        f.run()
    assert list(tmp_path.iterdir()) == []


def test_final_freeze_also_requires_reference_before_network(monkeypatch, tmp_path):
    monkeypatch.setattr(f, "STUDY", tmp_path)
    def unexpected(*args, **kwargs):
        raise AssertionError("Não pode chamar o modelo")
    monkeypatch.setattr(g, "Ollama", unexpected)
    with pytest.raises(ValueError, match="ratificação humana pendente"):
        f.freeze()
