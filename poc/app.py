from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from guardkids import BASE, Ollama, config, run_question

app = FastAPI(title="GuardKids — laboratório local", docs_url="/docs")


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=1500)
    policy: str = "ajustada"


@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE / "web" / "index.html").read_text(encoding="utf-8")


@app.get("/api/status")
def status():
    cfg = config()
    try:
        models = Ollama(cfg).identities()
        return {"ready": (BASE / "data" / "index.npz").exists() and all(m in models for m in [cfg["model"], cfg["embedding_model"]]),
                "model": cfg["model"], "embedding": cfg["embedding_model"], "policies": list(cfg["policies"])}
    except Exception:
        return {"ready": False, "message": "Ollama indisponível. Abra o Ollama e tente novamente."}


@app.post("/api/ask")
def ask(request: Question):
    try:
        record = run_question(request.question, request.policy)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    # O navegador recebe somente a resposta liberada. Textos rejeitados ficam nos registros do pesquisador.
    cited = set((record.get("generated") or {}).get("source_ids", [])) if record["action"] == "allow" else set()
    return {"id": record["id"], "answer": record["answer"], "action": record["action"],
            "valid": record["valid"], "seconds": record["seconds"], "policy": record["policy"],
            "sources": [{"id": c["id"], "source": c["source"], "page": c["printed_page"], "pdf_page": c["pdf_page"]}
                        for c in record["retrieved"] if c["id"] in cited],
            "stages": [{"name": c["stage"], "seconds": c["seconds"]} for c in record["calls"]]}
