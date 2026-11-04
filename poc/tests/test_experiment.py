import json
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guardkids as g
from experiment import export_experiment, summarize


def test_metrics_remain_pending_without_documented_human_review():
    row = {"policy": "ajustada", "valid": True, "action": "block"}
    assert summarize([row])["ajustada"]["T_RI"] is None
    row.update(human_inadequate="0", human_evaluator="Avaliador ficticio", human_date="2026-11-03", human_notes="Justificativa ficticia")
    assert summarize([row])["ajustada"]["T_RI"] == {"numerator": 0, "denominator": 1, "percent": 0}


def test_export_rejects_common_logs_and_invalid_ids(monkeypatch, tmp_path):
    monkeypatch.setattr(g, "BASE", tmp_path)
    logs = tmp_path / "runs"
    logs.mkdir()
    identifier = "a" * 32
    (logs / f"{identifier}.json").write_text(json.dumps({"id": identifier, "logging_mode": "minimized"}))
    with pytest.raises(ValueError, match="ficticias"):
        export_experiment([identifier], tmp_path / "out.zip")
    with pytest.raises(ValueError, match="invalido"):
        export_experiment(["../outro"], tmp_path / "out.zip")
    (logs / f"{identifier}.json").write_text(json.dumps({"id": "../outro", "synthetic": True, "logging_mode": "synthetic"}))
    with pytest.raises(ValueError, match="divergente"):
        export_experiment([identifier], tmp_path / "out.zip")


def test_export_includes_verified_snapshot(monkeypatch, tmp_path):
    monkeypatch.setattr(g, "BASE", tmp_path)
    identifier = "b" * 32
    snapshot = {"configuration": {}, "index": {"metadata": {"chunks": []}, "vectors": []}, "runtime": {}}
    snapshot_id = g.digest(snapshot)
    g.atomic_json(tmp_path / "runs/snapshots" / f"{snapshot_id}.json", snapshot)
    g.atomic_json(tmp_path / "runs" / f"{identifier}.json", {"id": identifier, "synthetic": True,
                  "logging_mode": "synthetic", "snapshot": snapshot_id})
    output = export_experiment([identifier], tmp_path / "out.zip")
    with zipfile.ZipFile(output) as archive:
        assert f"snapshots/{snapshot_id}.json" in archive.namelist()
        assert f"runs/{identifier}.json" in archive.namelist()
