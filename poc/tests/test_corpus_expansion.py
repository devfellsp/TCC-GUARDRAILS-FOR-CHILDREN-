import collections
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
VERSION = ROOT / "poc/versions/GK-P2.2-dev"
sys.path.insert(0, str(ROOT / "poc"))
import guardkids as baseline


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


expanded = load("guardkids_expanded", VERSION / "guardkids.py")


def test_baseline_files_and_runtime_remain_unchanged():
    saved = baseline.read_json(ROOT / "poc/versions/GK-P2.1-dev/preservacao.json")
    for name, expected in saved["protected_files"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    assert baseline.BASE == ROOT / "poc" and baseline.config()["study_version"] == "GK-P2.1-dev"
    assert expanded.BASE == VERSION and expanded.ROOT == ROOT


def test_expanded_corpus_preserves_eight_original_blocks_and_adds_ten_literal_excerpts():
    old, _, _ = baseline.extract_corpus(baseline.config())
    new, _, _ = expanded.extract_corpus(expanded.config())
    assert len(new) == len({x["id"] for x in new}) == 18
    assert collections.Counter(x["channel"] for x in new) == {"ciencias": 5, "historia": 6, "geografia": 6, "geral": 1}
    by_id = {x["id"]: x for x in new}
    for chunk in old:
        assert by_id[chunk["id"]] == chunk
    selected = expanded.read_json(VERSION / "recortes_selecionados.json")["passages"]
    assert len(selected) == 10
    for passage in selected:
        chunk = by_id[passage["id"] + "-1"]
        assert chunk["channel"] == passage["channel"]
        assert chunk["text"] == passage["literal_text"]
        assert 80 <= len(chunk["text"]) <= 850


@pytest.mark.parametrize("problem", ["missing_channel", "source_hash", "text_hash", "duplicate_id"])
def test_manifest_inconsistencies_are_rejected_before_indexing(problem, tmp_path, monkeypatch):
    manifest = expanded.read_json(VERSION / "corpus_manifest.json")
    added = manifest["sources"][-1]
    if problem == "missing_channel": added.pop("channel")
    if problem == "source_hash": added["source_sha256"] = "0" * 64
    if problem == "text_hash": added["passages"][0]["text_sha256"] = "0" * 64
    if problem == "duplicate_id": added["passages"][1]["id"] = added["passages"][0]["id"]
    (tmp_path / "corpus_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(expanded, "BASE", tmp_path)
    with pytest.raises(ValueError): expanded.extract_corpus(expanded.config() if (tmp_path / "config.json").exists() else baseline.config())


def test_competing_passages_are_filtered_by_chat_before_top_k(monkeypatch):
    cfg = expanded.config()
    chunks, _, _ = expanded.extract_corpus(cfg)
    vectors = np.array([[.7 if x["channel"] == "historia" else 1, 0] for x in chunks])
    monkeypatch.setattr(expanded, "load_index", lambda *a: ({"chunks": chunks}, vectors, "test-index"))
    class Client:
        def identities(self): return {}
        def check_budget(self): pass
        def embed(self, texts): return np.array([[1, 0]])
    selected, _ = expanded.retrieve("pergunta fictícia", cfg, Client(), "historia")
    assert len(selected) == 3 and {x["channel"] for x in selected} == {"historia"}


def test_new_cases_are_balanced_without_reusing_reserved_questions(monkeypatch):
    monkeypatch.setitem(sys.modules, "guardkids", expanded)
    runner = load("expansion_runner_schedule", VERSION / "run_expansion.py")
    cases = expanded.read_json(VERSION / "development_cases.json")
    reserved = baseline.read_json(ROOT / "avaliacao/final_multichat_v1/casos.json")
    assert not {c["question"] for c in cases} & {c["question"] for c in reserved}
    agenda = runner.schedule(cases)
    assert len(agenda) == 32 and agenda == runner.schedule(cases)
    assert collections.Counter(x["response_style"] for x in agenda) == {"padrao": 16, "passo_a_passo": 16}


def test_index_can_be_restored_without_inference_or_touching_baseline(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "guardkids", expanded)
    restore = load("expansion_restore", VERSION / "restore_index.py")
    for name in ["config.json", "corpus_manifest.json"]: shutil.copyfile(VERSION / name, tmp_path / name)
    shutil.copytree(VERSION / "indice_preservado", tmp_path / "indice_preservado")
    expected = expanded.read_json(tmp_path / "indice_preservado/current.json")["id"]
    monkeypatch.setattr(expanded, "BASE", tmp_path)
    assert restore.restore() == expected
    assert expanded.load_index(expanded.config())[2] == expected


def test_development_runner_preserves_loss_and_rejects_selective_rerun(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "guardkids", expanded)
    runner = load("expansion_runner_loss", VERSION / "run_expansion.py")
    snapshot = "a" * 64
    item = {"order": 1, "case_id": "test", "channel": "historia", "group": "educativa",
            "question": "Pergunta fictícia", "policy": "comum", "response_style": "padrao",
            "expected_action_proposed": "allow", "reference_ids": "", "repetition": 1}
    plan = {"inputs": {}, "snapshot": snapshot, "version": "GK-P2.2-dev", "planned_attempts": 1,
            "questions": 1, "index_id": "i", "agenda": [item]}
    plan["plan_id"] = expanded.digest(plan)
    folder = tmp_path / "lote";folder.mkdir()
    expanded.atomic_json(folder / "plano.json", plan)
    monkeypatch.setattr(expanded, "BASE", tmp_path)
    monkeypatch.setattr(expanded, "config", lambda: {})
    monkeypatch.setattr(expanded, "save_snapshot", lambda cfg: snapshot)
    monkeypatch.setattr(runner, "fingerprint", lambda: {})
    record = {"id": "1" * 32, "snapshot": snapshot, "valid": False, "action": "technical_error",
              "answer": "Indisponível", "seconds": 1, "retrieved": [], "error": "TimeoutError"}
    expanded.atomic_json(tmp_path / "runs" / f"{record['id']}.json", record)
    expanded.atomic_json(tmp_path / "runs/snapshots" / f"{snapshot}.json", {})
    calls = []
    def fake(*a, **kw): calls.append(1);return record
    monkeypatch.setattr(expanded, "run_question", fake)
    runner.execute(folder)
    with (folder / "resultados.csv").open(encoding="utf-8-sig", newline="") as stream:rows=list(csv.DictReader(stream))
    assert len(rows) == len(calls) == 1 and rows[0]["valid"] == "False"
    assert rows[0]["human_reviewer"] == rows[0]["human_source_support"] == ""
    with pytest.raises(ValueError, match="não repetir"): runner.execute(folder)
    assert len(calls) == 1


def test_expanded_interface_identifies_version_and_uses_separate_local_origin(monkeypatch):
    from fastapi.testclient import TestClient
    monkeypatch.setitem(sys.modules, "guardkids", expanded)
    app = load("expanded_web", VERSION / "app.py")
    def busy(*args, **kwargs): raise expanded.BusyError("Cenário simulado")
    monkeypatch.setattr(app, "run_question", busy)
    with TestClient(app.app, base_url="http://127.0.0.1:8766") as client:
        assert "GK-P2.2-dev" in client.get("/").text
        assert client.post("/api/ask", json={"question": "Teste fictício"},
                           headers={"origin": "http://127.0.0.1:8766"}).status_code == 429
        assert client.post("/api/ask", json={"question": "Teste fictício"},
                           headers={"origin": "http://127.0.0.1:8765"}).status_code == 403
