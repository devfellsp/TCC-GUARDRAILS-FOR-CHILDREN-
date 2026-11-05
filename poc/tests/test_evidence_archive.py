import csv
import json
from pathlib import Path
import runpy
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import archive_multichat_evidence as a
import package_overleaf as package


@pytest.fixture
def source(tmp_path):
    folder = tmp_path / a.BATCH
    folder.mkdir(parents=True)
    runs = tmp_path / "poc/runs"
    (runs / "snapshots").mkdir(parents=True)
    snapshot = {"index": {"id": "b" * 64}, "runtime": {"python": "teste", "platform": "teste"}}
    identifier = a.identity(snapshot)
    a.write(runs / "snapshots" / f"{identifier}.json", snapshot)
    rows = []
    for i in range(2):
        record = {"id": f"{i:032x}", "case_id": f"caso-{i}", "channel": "ciencias", "policy": "comum",
                  "response_style": "padrao", "action": "allow", "valid": True, "seconds": 1,
                  "snapshot": identifier, "index_hash": "b" * 64, "synthetic": True,
                  "logging_mode": "synthetic", "model_digests": {"modelo-teste": "digest-teste"},
                  "ollama_version": "teste"}
        a.write(runs / f"{record['id']}.json", record)
        rows.append({**{k: record[k] for k in ("case_id", "channel", "policy", "response_style", "valid", "seconds", "snapshot")},
                     "run_id": record["id"], "observed": record["action"]})
    with (folder / "resultados.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    a.write(folder / "resumo.json", {"executions": 2, "snapshot": identifier})
    for name in ("agenda.json", "revisao_assistida_IA.json"):
        a.write(folder / name, {})
    (folder / "REVISAO_DAS_RESPOSTAS.md").write_text("Cenário fictício de teste", encoding="utf-8")
    a.write(tmp_path / "avaliacao/evidencias/ambiente_hardware.json", {"note": "teste"})
    return tmp_path


def test_archival_copies_bytes_and_is_idempotent_without_mutating_sources(source):
    originals = {str(p): p.read_bytes() for p in (source / "poc/runs").rglob("*.json")}
    manifest = a.archive(source)
    assert manifest["executions"] == 2
    assert manifest == a.archive(source) == a.verify(source)
    assert originals == {str(p): p.read_bytes() for p in (source / "poc/runs").rglob("*.json")}
    for path in (source / a.BATCH / "runs").glob("*.json"):
        assert path.read_bytes() == (source / "poc/runs" / path.name).read_bytes()


def test_non_synthetic_records_are_rejected_before_copying(source):
    path = next((source / "poc/runs").glob("*.json"))
    value = a.read(path)
    value["synthetic"] = False
    a.write(path, value)
    with pytest.raises(ValueError, match="fictícios"):
        a.archive(source)
    assert not (source / a.BATCH / "runs").exists()


def test_corrupted_archive_is_rejected_not_silently_replaced(source):
    a.archive(source)
    path = next((source / a.BATCH / "runs").glob("*.json"))
    path.write_text("alterado", encoding="utf-8")
    with pytest.raises(ValueError, match="divergente"):
        a.archive(source)
    assert path.read_text(encoding="utf-8") == "alterado"


def test_legacy_generator_cannot_overwrite_current_manuscript():
    before = (ROOT / "main.tex").read_bytes()
    with pytest.raises(SystemExit, match="desativado"):
        runpy.run_path(str(ROOT / "tools/update_manuscript.py"), run_name="__main__")
    assert (ROOT / "main.tex").read_bytes() == before


def test_delivery_contains_auditable_records_but_not_generic_local_runs(tmp_path):
    # Exercita a seleção real de arquivos, escrevendo o ZIP somente na pasta do teste.
    import shutil
    root = tmp_path / "project"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(
        ".git", ".cache", ".venv", "runs", "data", "__pycache__", "*.zip",
        "historico", "Livros_Didadicos", "benchmarks_e_datasets", "artigos_e_guias", "outputs"))
    # A exclusão genérica de runs acima remove também as cópias arquivadas: restituir apenas estas.
    shutil.copytree(ROOT / a.BATCH / "runs", root / a.BATCH / "runs")
    for folder in (ROOT / "avaliacao/evidencias").glob("desenvolvimento_20261103_*"):
        shutil.copytree(folder / "runs", root / folder.relative_to(ROOT) / "runs")
    local = root / "poc/runs"
    local.mkdir(parents=True)
    (local / "registro_nao_selecionado.json").write_text("privado", encoding="utf-8")
    target = package.build(root)
    with zipfile.ZipFile(target) as archive:
        names = archive.namelist()
        assert str(a.BATCH).replace("\\", "/") + "/agenda.json" in names
        assert any("/snapshots/4531f5b01c5b" in n for n in names)
        assert len([n for n in names if n.startswith(a.BATCH.as_posix() + "/runs/")]) == 32
        assert not any(n.startswith("poc/runs/") for n in names)
        assert not any(n.startswith("poc/data/") for n in names)
        assert not any(n.startswith(".venv/") or n.startswith("poc/.venv/") for n in names)
        assert all(archive.read(n) == (root / n).read_bytes() for n in names)
