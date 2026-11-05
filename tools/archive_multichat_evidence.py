"""Arquiva evidências sintéticas existentes; não executa modelos nem altera originais."""
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BATCH = Path("avaliacao/evidencias/multichat_20261104_revisado")
MANIFEST = "manifesto_rastreabilidade.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify(root=ROOT, batch=BATCH):
    folder = root / batch
    manifest = read(folder / MANIFEST)
    for name, expected in manifest["files"].items():
        path = (folder / name).resolve()
        path.relative_to(folder.resolve())
        if sha(path.read_bytes()) != expected:
            raise ValueError("Arquivo arquivado divergente: " + name)
    identifier = manifest["snapshot"]
    snapshot = read(folder / "snapshots" / f"{identifier}.json")
    if identity(snapshot) != identifier or snapshot["index"]["id"] != manifest["index_id"]:
        raise ValueError("Snapshot ou índice arquivado divergente")
    with (folder / "resultados.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    expected_runs = {r["run_id"] + ".json" for r in rows}
    if ({p.name for p in (folder / "runs").glob("*.json")} != expected_runs
            or len(rows) != manifest["executions"]):
        raise ValueError("Cobertura dos registros arquivados divergente")
    return manifest


def archive(root=ROOT, batch=BATCH):
    root = Path(root).resolve()
    folder = (root / batch).resolve()
    folder.relative_to(root)
    if (folder / MANIFEST).exists():
        return verify(root, batch)
    with (folder / "resultados.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    summary = read(folder / "resumo.json")
    if not rows or len(rows) != summary["executions"] or len({r["run_id"] for r in rows}) != len(rows):
        raise ValueError("Lote incompleto ou com registros duplicados")
    snapshots = {r["snapshot"] for r in rows}
    if len(snapshots) != 1 or snapshots != {summary["snapshot"]}:
        raise ValueError("Lote mistura snapshots")
    identifier = summary["snapshot"]
    if not re.fullmatch(r"[0-9a-f]{64}", identifier):
        raise ValueError("Identificador de snapshot inválido")
    snapshot_path = root / "poc/runs/snapshots" / f"{identifier}.json"
    snapshot = read(snapshot_path)
    if identity(snapshot) != identifier:
        raise ValueError("Snapshot alterado")
    index_id = snapshot["index"]["id"]
    copies = {f"snapshots/{identifier}.json": snapshot_path}
    records = []
    for row in rows:
        run_id = row["run_id"]
        if not re.fullmatch(r"[0-9a-f]{32}", run_id):
            raise ValueError("Identificador de execução inválido")
        path = root / "poc/runs" / f"{run_id}.json"
        record = read(path)
        if record.get("synthetic") is not True or record.get("logging_mode") != "synthetic":
            raise ValueError("Somente registros explicitamente fictícios podem ser arquivados")
        if record["id"] != run_id or record["snapshot"] != identifier:
            raise ValueError("Execução não corresponde ao lote")
        for field in ("case_id", "channel", "policy", "response_style"):
            if record[field] != row[field]:
                raise ValueError("Condição de execução divergente: " + field)
        if (record["action"] != row["observed"] or str(record["valid"]).lower() != row["valid"].lower()
                or float(record["seconds"]) != float(row["seconds"])):
            raise ValueError("Resultado CSV diverge do registro original")
        if record.get("index_hash") not in (None, index_id):
            raise ValueError("Índice da execução diverge do snapshot")
        copies[f"runs/{run_id}.json"] = path
        records.append(record)
    models = [r["model_digests"] for r in records if r.get("model_digests")]
    if not models or any(m != models[0] for m in models):
        raise ValueError("Identidades dos modelos inconsistentes")
    hardware = read(root / "avaliacao/evidencias/ambiente_hardware.json")
    originals = ["agenda.json", "resultados.csv", "resumo.json", "revisao_assistida_IA.json", "REVISAO_DAS_RESPOSTAS.md"]
    for name in originals:
        (folder / name).read_bytes()
    # Conferir tudo antes de copiar. Não substituir cópias anteriores diferentes.
    for name, source in copies.items():
        target = folder / name
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError("Cópia anterior divergente: " + name)
    for name, source in copies.items():
        target = folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(source, target)
    environment = {"snapshot": identifier, "index_id": index_id,
        "python": snapshot["runtime"]["python"], "platform": snapshot["runtime"]["platform"],
        "ollama_versions": sorted({r["ollama_version"] for r in records if r.get("ollama_version")}),
        "model_digests": models[0], "hardware_source": "avaliacao/evidencias/ambiente_hardware.json",
        "hardware": hardware,
        "note": "Hardware de referência registrado na documentação local; sem monitoramento por tentativa. "
                "Não constitui comparação controlada de desempenho."}
    write(folder / "ambiente_lote.json", environment)
    names = [*originals, "ambiente_lote.json", *copies]
    manifest = {"executions": len(rows), "snapshot": identifier, "index_id": index_id,
                "nature": "cópias byte a byte de registros fictícios existentes; sem nova inferência",
                "source": "poc/runs", "human_review": "pendente",
                "files": {name: sha((folder / name).read_bytes()) for name in sorted(names)}}
    write(folder / MANIFEST, manifest)
    return verify(root, batch)


if __name__ == "__main__":
    value = archive()
    print(json.dumps({k: value[k] for k in ("executions", "snapshot", "index_id")}, indent=2))
