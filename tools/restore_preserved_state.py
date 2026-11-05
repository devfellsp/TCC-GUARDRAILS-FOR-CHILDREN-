"""Reconstitui estado local ignorado pelo Git usando somente cópias preservadas.

Sem modelos, rede ou sobrescrita de arquivos divergentes. O padrão só mostra
o plano; --apply cria os arquivos ausentes, inclusive no checkout de CI.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def plan(root=ROOT):
    copies = []
    for version in sorted((root / "poc/versions").glob("GK-P2.*-dev")):
        saved = version / "indice_preservado"
        if not (saved / "current.json").is_file():
            continue
        identifier = json.loads((saved / "current.json").read_text(encoding="utf-8-sig"))["id"]
        if not re.fullmatch(r"[0-9a-f]{64}", identifier):
            raise ValueError("Identificador de índice inválido")
        metadata = json.loads((saved / identifier / "chunks.json").read_text(encoding="utf-8-sig"))
        actual = hashlib.sha256(json.dumps(metadata, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        if actual != identifier:
            raise ValueError("Metadados preservados divergentes")
        base = root / "poc" if version.name == "GK-P2.1-dev" else version
        copies.append((saved / "current.json", base / "data/current.json"))
        for name in ("chunks.json", "index.npz"):
            copies.append((saved / identifier / name, base / "data/indices" / identifier / name))
    batches = [(root / "avaliacao/evidencias/multichat_20261104_revisado", root / "poc")]
    for number, prefix in ((2, "ampliacao"), (3, "correcoes"), (4, "correcoes"), (5, "correcoes")):
        batches.append((root / f"avaliacao/evidencias/{prefix}_GK_P2_{number}_dev_20261105",
                        root / f"poc/versions/GK-P2.{number}-dev"))
    for folder, base in batches:
        for source in sorted((folder / "runs").glob("*.json")):
            copies.append((source, base / "runs" / source.name))
        for source in sorted((folder / "snapshots").glob("*.json")):
            copies.append((source, base / "runs/snapshots" / source.name))
    for source, target in copies:
        if not source.is_file() or not source.resolve().is_relative_to(root.resolve()) or not target.resolve().is_relative_to(root.resolve()):
            raise ValueError("Caminho de restauração inválido")
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError(f"Arquivo existente divergente; nenhuma restauração aplicada: {target.relative_to(root)}")
    return copies


def restore(root=ROOT, apply=False):
    copies = plan(root)  # Confere todos os conflitos antes de criar qualquer arquivo.
    missing = [(source, target) for source, target in copies if not target.exists()]
    if apply:
        for source, target in missing:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(source.read_bytes())
    return {"checked_files": len(copies), "missing_files": len(missing), "created_files": len(missing) if apply else 0,
            "inference": False, "overwritten_files": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print(json.dumps(restore(apply=args.apply), ensure_ascii=True, indent=2))
