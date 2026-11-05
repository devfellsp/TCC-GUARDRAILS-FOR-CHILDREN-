import asyncio
import functools
import threading
import time
from typing import Literal

import anyio
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette.middleware.trustedhost import TrustedHostMiddleware

from guardkids import BASE, BusyError, Ollama, PersistenceError, config, load_index, run_question
from channels import CHANNELS

app = FastAPI(title="GuardKids GK-P2.6-dev — acervo ampliado", docs_url="/docs")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "[::1]"])
ORIGINS = {"http://127.0.0.1:8770", "http://localhost:8770", "http://[::1]:8770"}


class LocalRequests:
    """Valida origem e limita o corpo antes de a camada JSON alocar a mensagem."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] != "POST":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])
        origin = headers.get(b"origin")
        if ((origin is not None and origin.decode("latin-1") not in ORIGINS)
                or headers.get(b"sec-fetch-site") == b"cross-site"):
            return await JSONResponse({"detail": "Origem nao autorizada"}, 403)(scope, receive, send)
        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body.extend(message.get("body", b""))
            if len(body) > 8192:
                return await JSONResponse({"detail": "Requisicao muito grande"}, 413)(scope, receive, send)
            if not message.get("more_body", False):
                break
        consumed = False

        async def limited_receive():
            nonlocal consumed
            if not consumed:
                consumed = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        await self.app(scope, limited_receive, send)


app.add_middleware(LocalRequests)


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    question: str = Field(min_length=1, max_length=1500)
    policy: Literal["comum"] | None = None
    channel: str = Field(default="ciencias", json_schema_extra={"enum": list(CHANNELS)})
    response_style: Literal["padrao", "passo_a_passo"] = "padrao"

    @field_validator("channel")
    @classmethod
    def known_channel(cls, value):
        if value not in CHANNELS:
            raise ValueError("Materia desconhecida")
        return value


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse((BASE / "web" / "index.html").read_text(encoding="utf-8"), headers={"Cache-Control": "no-store"})


@app.get("/api/health")
async def health():
    return {"alive": True}


@app.get("/api/channels")
async def channels():
    return CHANNELS


@app.get("/api/status")
def status():
    try:
        cfg = config()
        client = Ollama(cfg, deadline=time.monotonic() + cfg["runtime"]["status_timeout_seconds"])
        models = client.identities()
        if not all(m in models for m in [cfg["model"], cfg["embedding_model"]]):
            raise ValueError("Modelos ausentes")
        _, _, index_id = load_index(cfg, models)
        return {"ready": True, "index_id": index_id, "model": cfg["model"],
                "embedding": cfg["embedding_model"], "policies": list(cfg["policies"]), "version": cfg["study_version"],
                "request_timeout_ms": int((cfg["runtime"]["deadline_seconds"] + 10) * 1000)}
    except Exception:
        return {"ready": False, "message": "Confira o Ollama, os modelos e a integridade do indice. Consulte LEIA-ME.md."}


def public_result(record):
    # O navegador recebe somente a resposta liberada. Textos rejeitados ficam nos registros do pesquisador.
    cited = set((record.get("generated") or {}).get("source_ids", [])) if record["action"] == "allow" else set()
    return {"from_source": record.get("final_origin") == "extractive_fallback", "id": record["id"], "answer": record["answer"], "action": record["action"],
            "valid": record["valid"], "seconds": record["seconds"], "policy": record["policy"], "channel": record.get("channel", "ciencias"),
            "response_style": record.get("response_style", "padrao"),
            "sources": [{"id": c["id"], "source": c["source"], "page": c["printed_page"], "pdf_page": c["pdf_page"]}
                        for c in record["retrieved"] if c["id"] in cited],
            "stages": [{"name": c["stage"], "seconds": c["seconds"]} for c in record["calls"]]}


@app.post("/api/ask")
async def ask(question: Question, request: Request):
    cancelled = threading.Event()
    task = asyncio.create_task(anyio.to_thread.run_sync(functools.partial(
        run_question, question.question, question.policy, cancelled=cancelled, channel=question.channel, response_style=question.response_style)))
    try:
        while not task.done():
            await asyncio.wait({task}, timeout=0.2)
            if not task.done() and await request.is_disconnected():
                cancelled.set()
                task.add_done_callback(consume_task)
                return JSONResponse({"detail": "Execucao cancelada"}, status_code=499)
        return public_result(task.result())
    except asyncio.CancelledError:
        cancelled.set()
        task.add_done_callback(consume_task)
        raise
    except BusyError as exc:
        raise HTTPException(429, str(exc), headers={"Retry-After": "2"}) from exc
    except PersistenceError as exc:
        raise HTTPException(503, "Nao foi possivel registrar a tentativa. A resposta foi retida.") from exc
    except ValueError as exc:
        raise HTTPException(400, "Pergunta ou configuracao invalida") from exc


def consume_task(task):
    if not task.cancelled():
        task.exception()
