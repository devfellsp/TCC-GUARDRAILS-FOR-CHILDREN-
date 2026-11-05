import copy
import csv
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import final_metrics as m
import final_multichat as f


def judgment(identifier, role):
    return {"review_id": identifier, "papel": role, "avaliador": f"Revisor fictício de teste: {role}",
            "data": "2026-11-04", "justificativa": "Cenário exclusivamente simulado",
            "seguranca": "adequado", "tratamento": "adequado", "factualidade": "integral",
            "sustentacao": "integral", "clareza": "integral", "qualidade_exemplos": "integral"}


@pytest.fixture
def data():
    cases, protocol = f.inputs()
    agenda = f.schedule(cases, protocol["seed"])
    results = [{**r, "run_id": f"teste-{i}", "valid": True,
                "action": "allow" if r["group"] == "educativa" else "block"}
               for i, r in enumerate(agenda)]
    return {"agenda": agenda, "results": results,
            "primary": [judgment(r["observation_id"], "primario") for r in agenda],
            "secondary": [judgment(r["observation_id"], "secundario") for r in agenda if r["secondary_review"]],
            "reconciliation": [{"review_id": r["observation_id"], "papel": "conciliacao"}
                               for r in agenda if r["secondary_review"]],
            "human_reference_confirmed": True}


def educational(data, selected=False):
    return next(r for r in data["results"] if r["group"] == "educativa"
                and r["response_style"] == "padrao" and r["secondary_review"] == selected)


def change(dataset, row, **values):
    for name in ("primary", "secondary"):
        for review in dataset[name]:
            if review["review_id"] == row["observation_id"]:
                review.update(values)


def style(result):
    return result["by_style"]["padrao"]


def test_complete_human_review_releases_eight_of_eight_and_paired_families(data):
    out = m.summary(**data)
    assert out["released"]
    assert style(out)["ascs_conclusive"] == {"numerator": 8, "denominator": 8, "rate": 1}
    assert style(out)["ascs_opportunity"]["rate"] == 1
    assert all(x["planned"] == 2 for x in style(out)["by_chat"].values())
    assert all(x["ascs_conclusive"]["rate"] == 1 for x in style(out)["by_family"].values())
    assert out["paired"]["complete"] == 8 and out["paired"]["mean_difference"] == 0


@pytest.mark.parametrize("action", ["block", "redirect", "safe_guidance"])
def test_undue_refusal_stays_in_denominator_with_nonapplicable_dimensions(data, action):
    row = educational(data)
    row["action"] = action
    change(data, row, tratamento="inadequado", factualidade="não aplicável", sustentacao="não aplicável")
    out = m.summary(**data)
    assert style(out)["ascs_conclusive"] == {"numerator": 7, "denominator": 8, "rate": 7/8}
    assert out["paired"]["mean_difference"] == 1/8


def test_loss_and_inconclusive_have_distinct_counts_and_fixed_opportunity_denominator(data):
    row = educational(data)
    row.update(valid=False, action="technical_error")
    for name in ("primary", "secondary"):
        data[name] = [r for r in data[name] if r["review_id"] != row["observation_id"]]
    other = next(r for r in data["results"] if r["group"] == "educativa"
                 and r["response_style"] == "padrao" and r is not row)
    change(data, other, sustentacao="inconclusivo")
    out = m.summary(**data)
    assert out["released"]
    assert style(out)["technical_losses"] == style(out)["inconclusive"] == 1
    assert style(out)["ascs_conclusive"] == {"numerator": 6, "denominator": 6, "rate": 1}
    assert style(out)["ascs_opportunity"] == {"numerator": 6, "denominator": 8, "rate": .75}
    assert out["paired"]["excluded"] == 2


def test_known_failure_remains_conclusive_despite_other_inconclusive_dimension(data):
    row = educational(data)
    change(data, row, seguranca="inadequado", sustentacao="inconclusivo")
    assert style(m.summary(**data))["conclusive_failures"] == 1


@pytest.mark.parametrize("missing", ["avaliador", "data", "justificativa", "clareza", "sustentacao"])
def test_missing_human_fields_hold_all_rates_pending(data, missing):
    row = educational(data)
    change(data, row, **{missing: ""})
    out = m.summary(**data)
    assert not out["released"] and style(out)["review_pending"] == 1
    assert style(out)["ascs_conclusive"]["rate"] is None
    assert style(out)["ascs_opportunity"]["rate"] is None


def test_unexecuted_and_unratified_are_never_final_zero_percent(data):
    data["results"] = []
    data["human_reference_confirmed"] = False
    out = m.summary(**data)
    assert out["counts"] == {"not_executed": 64}
    assert style(out)["ascs_opportunity"]["rate"] is None
    data["results"] = []
    assert not out["released"]


def test_completed_reviews_still_require_reference_ratification(data):
    data["human_reference_confirmed"] = False
    assert style(m.summary(**data))["ascs_opportunity"]["rate"] is None


def test_partial_batch_and_missing_secondary_cannot_release_final_rates(data):
    data["results"].pop()
    out = m.summary(**data)
    assert not out["released"] and out["counts"]["not_executed"] == 1
    assert style(out)["ascs_opportunity"]["denominator"] == 8
    assert style(out)["ascs_opportunity"]["rate"] is None


def test_primary_agreement_cannot_replace_required_second_review(data):
    data["secondary"].pop()
    out = m.summary(**data)
    assert not out["released"] and out["counts"]["pending"] == 1


def test_same_declared_reviewer_cannot_supply_both_independent_reviews(data):
    row = educational(data, selected=True)
    a = next(r for r in data["primary"] if r["review_id"] == row["observation_id"])
    b = next(r for r in data["secondary"] if r["review_id"] == row["observation_id"])
    b["avaliador"] = a["avaliador"]
    with pytest.raises(ValueError, match="outro avaliador"):
        m.summary(**data)


def test_all_educational_losses_have_zero_demonstrated_success_not_zero_conclusive_rate(data):
    ids = {r["observation_id"] for r in data["results"] if r["group"] == "educativa"}
    for row in data["results"]:
        if row["observation_id"] in ids:
            row.update(valid=False, action="technical_error")
    for name in ("primary", "secondary"):
        data[name] = [r for r in data[name] if r["review_id"] not in ids]
    out = m.summary(**data)
    assert out["released"] and style(out)["technical_losses"] == 8
    assert style(out)["ascs_conclusive"] == {"numerator": 0, "denominator": 0, "rate": None}
    assert style(out)["ascs_opportunity"]["rate"] == 0


def test_nonapplicable_factuality_does_not_create_success(data):
    row = educational(data)
    change(data, row, factualidade="não aplicável")
    assert style(m.summary(**data))["inconclusive"] == 1


def test_unselected_secondary_review_is_rejected(data):
    row = educational(data, selected=False)
    data["secondary"].append(judgment(row["observation_id"], "secundario"))
    with pytest.raises(ValueError, match="desconhecido"):
        m.summary(**data)


def test_secondary_disagreement_needs_documented_dimension_specific_reconciliation(data):
    row = educational(data, selected=True)
    second = next(r for r in data["secondary"] if r["review_id"] == row["observation_id"])
    second["sustentacao"] = "parcial"
    assert not m.summary(**data)["released"]
    c = next(r for r in data["reconciliation"] if r["review_id"] == row["observation_id"])
    c.update(avaliador="Conciliador fictício", data="2026-11-04", justificativa="Divergência simulada",
             dimensoes_divergentes="sustentacao", sustentacao="inconclusivo")
    out = m.summary(**data)
    assert out["released"] and style(out)["inconclusive"] == 1
    family = style(out)["by_family"][row["family_id"]]
    assert family["ascs_conclusive"]["rate"] is None  # Não renormalizar a família incompleta.
    assert family["ascs_opportunity"]["rate"] == .5
    c["seguranca"] = "inadequado"
    with pytest.raises(ValueError, match="concordante"):
        m.summary(**data)


@pytest.mark.parametrize("mistake", ["duplicate_result", "duplicate_review", "wrong_case", "invalid_label",
                                    "invalid_date", "loss_with_review", "contradictory_route"])
def test_malformed_or_contradictory_inputs_fail_explicitly(data, mistake):
    row = educational(data)
    if mistake == "duplicate_result": data["results"].append(copy.deepcopy(row))
    if mistake == "duplicate_review": data["primary"].append(copy.deepcopy(data["primary"][0]))
    if mistake == "wrong_case": row["case_id"] = "outro-lote"
    if mistake == "invalid_label": change(data, row, sustentacao="aprovado automaticamente")
    if mistake == "invalid_date": change(data, row, data="2026-02-30")
    if mistake == "loss_with_review": row.update(valid=False, action="technical_error")
    if mistake == "contradictory_route": row["action"] = "redirect"
    with pytest.raises(ValueError): m.summary(**data)


def test_pending_report_reads_actual_templates_without_network_or_mutation(monkeypatch):
    def unexpected(*args, **kwargs): raise AssertionError("Não deve inferir nem ratificar")
    monkeypatch.setattr(f.g, "Ollama", unexpected)
    monkeypatch.setattr(f.g, "atomic_json", unexpected)
    monkeypatch.setattr(f, "ratify", unexpected)
    out = m.report(f.STUDY)
    assert not out["released"] and out["planned_total"] == 64
    assert style(out)["ascs_opportunity"] == {"numerator": 0, "denominator": 8, "rate": None}


def test_batch_without_ratified_reference_is_rejected_before_results(tmp_path):
    with pytest.raises(FileNotFoundError): m.report(f.STUDY, tmp_path)


def test_csv_batch_roundtrip_requires_matching_ratification_and_freeze(data, tmp_path, monkeypatch):
    root = tmp_path
    study = root / "avaliacao/final_multichat_v1"
    study.mkdir(parents=True)
    batch = study / "lote_ficticio_teste"
    batch.mkdir()
    cases, protocol = f.inputs()
    def write_json(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    def write_csv(path, rows):
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    write_json(study / "casos.json", cases)
    write_json(study / "protocolo.json", protocol)
    write_json(study / "agenda_planejada.json", data["agenda"])
    write_json(batch / "agenda.json", data["agenda"])
    reference = [{**{k: c[k] for k in ("id", "family_id", "channel", "group", "category", "question", "expected_action")},
                  "reference_ids": ";".join(c["reference_ids"]), "human_confirmed": "sim",
                  "human_reviewer": "Responsável fictício de teste", "human_date": "2026-11-04",
                  "human_reason": "Declaração simulada, sem inferência"} for c in cases]
    reference_file = study / "referencia_humana.csv"
    write_csv(reference_file, reference)
    write_json(study / "referencia_ratificada.json", {"case_hash": f.g.digest(cases),
               "csv_hash": f.g.digest(reference_file.read_bytes()), "csv_file": str(reference_file)})
    hashes = {"avaliacao/final_multichat_v1/" + n: f.g.digest((study / n).read_bytes())
              for n in ("casos.json", "protocolo.json", "referencia_ratificada.json")}
    frozen = {"sources": hashes}
    write_json(batch / "congelamento.json", {"id": f.g.digest(frozen), "value": frozen})
    write_csv(batch / "resultados.csv", data["results"])
    for filename, name in [("parecer_primario.csv", "primary"), ("parecer_secundario.csv", "secondary"),
                           ("conciliacao.csv", "reconciliation")]:
        write_csv(study / filename, data[name])
    monkeypatch.setattr(f.g, "ROOT", root)
    assert m.report(study, batch)["released"]
    assert style(m.report(study, batch))["ascs_opportunity"]["rate"] == 1
    protocol["seed"] += 1
    write_json(study / "protocolo.json", protocol)
    with pytest.raises(ValueError): m.report(study, batch)
