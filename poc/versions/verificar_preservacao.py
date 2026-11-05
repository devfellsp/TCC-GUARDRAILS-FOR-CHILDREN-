"""Confere os arquivos da versão do TCC sem restaurar, sobrescrever ou inferir."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def verify():
    saved = json.loads((ROOT / "poc/versions/GK-P2.1-dev/preservacao.json").read_text(encoding="utf-8"))
    changed = [name for name, digest in saved["protected_files"].items()
               if not (ROOT / name).exists() or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest]
    return {"version": "GK-P2.1-dev", "checked_files": len(saved["protected_files"]), "changed_files": changed}


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(1 if result["changed_files"] else 0)
