"""Inicia a versao local depois de conferir modelo e indice."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import time
from urllib.request import urlopen

BASE = Path(__file__).resolve().parent


def tags():
    with urlopen("http://127.0.0.1:11434/api/tags", timeout=3) as response:
        return json.load(response)


def ensure_ollama():
    try:
        return tags()
    except OSError:
        binary = shutil.which("ollama")
        if not binary and os.name == "nt":
            candidate = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Ollama/ollama.exe"
            if candidate.is_file():
                binary = str(candidate)
        if not binary:
            raise RuntimeError("Ollama nao encontrado. Instale ou abra o Ollama e tente novamente.")
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        with (BASE / "ollama-start.log").open("ab") as log:
            subprocess.Popen([binary, "serve"], stdout=log, stderr=log, creationflags=flags)
        for _ in range(30):
            time.sleep(1)
            try:
                return tags()
            except OSError:
                pass
        raise RuntimeError("O Ollama nao ficou disponivel em 30 segundos.")


def prepare():
    from guardkids import config, load_index
    cfg = config()
    models = {m["name"] for m in ensure_ollama()["models"]}
    missing = {cfg["model"], cfg["embedding_model"]} - models
    if missing:
        raise RuntimeError("Modelos locais ausentes: " + ", ".join(sorted(missing)))
    if not (BASE / "data/current.json").exists():
        from restore_index import restore
        restore()
    load_index(cfg)


if __name__ == "__main__":
    try:
        prepare()
    except Exception as exc:
        print("Nao foi possivel preparar o GuardKids: " + str(exc))
        sys.exit(1)
    print("GuardKids GK-P2.6-dev: http://127.0.0.1:8770")
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8770, app_dir=str(BASE))
