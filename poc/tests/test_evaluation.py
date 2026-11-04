import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import evaluation as e


def test_schedule_paired_balanced_and_reproducible():
    cases = [{"case_id": f"c{i}", "family_id": f"f{i//2}"} for i in range(8)]
    agenda = e.schedule(cases)
    assert agenda == e.schedule(cases)
    assert len(agenda) == 32 and len({r["observation_id"] for r in agenda}) == 32
    for case in cases:
        entries = [r for r in agenda if r["case_id"] == case["case_id"]]
        assert entries[0]["policy"] != entries[2]["policy"]


def test_metrics_do_not_treat_ai_or_losses_as_safe():
    rows = [{"case_id": "x", "repetition": 1, "group": "G2", "category": "normal", "policy": p, "valid": True,
             "natureza": "assistida_IA", "seguranca": "adequada", "avaliador": "IA", "data": "2026-11-03", "justificativa": "exemplo"} for p in ["referencia", "ajustada"]]
    result = e.metric_summary(rows)
    assert result["ajustada/G2"]["inadequate_rate"] is None
    assert result["paired"]["G2"]["complete_safety_pairs"] == 0
    for row in rows:
        row.update(natureza="humana", factual="integral", fidelidade="integral", atendimento="integral", tratamento="adequado")
    rows[0]["atendimento"] = "ausente"
    result = e.metric_summary(rows)
    assert result["paired"]["G2"]["ASCS_difference"] == 1
    assert result["ajustada/cat:normal"]["inadequate_denominator"] == 1
    rows[1]["valid"] = False
    result = e.metric_summary(rows)
    assert result["ajustada/G2"]["technical_losses"] == 1
    assert result["paired"]["G2"]["safety_difference_adjusted_minus_reference"] is None


def test_final_rejects_unratified_reference(monkeypatch, tmp_path):
    monkeypatch.setattr(e, "STUDY", tmp_path)
    e.g.atomic_json(tmp_path / "protocolo.json", {})
    monkeypatch.setattr(e, "verify_freeze", lambda: ("id", {"human_reference_status": "pendente"}))
    with pytest.raises(ValueError, match="nao liberada"):
        e.evaluation()


def test_unexecuted_rows_are_not_technical_losses():
    row = {"case_id": "planned", "repetition": 1, "policy": "ajustada", "group": "G1", "valid": "pendente"}
    result = e.metric_summary([row])["ajustada/G1"]
    assert result["technical_losses"] == 0 and result["not_executed"] == 1
    assert result["metrics"]["ASCS"]["opportunity_rate"] is None
