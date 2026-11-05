"""Configuracao local validada antes de iniciar qualquer inferencia."""
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)


class GenerationSettings(StrictModel):
    temperature: float = Field(ge=0, le=2)
    seed: int
    top_p: float = Field(gt=0, le=1)
    repeat_penalty: float = Field(gt=0)
    num_ctx: int = Field(ge=1024, le=32768)
    num_predict: int = Field(gt=0, le=4096)


class RetrievalSettings(StrictModel):
    top_k: int = Field(ge=1, le=20)
    min_similarity: float = Field(ge=-1, le=1)
    chunk_chars: int = Field(ge=80, le=8000)
    overlap_sentences: int = Field(ge=0, le=10)


class Policy(StrictModel):
    allow_educational_predation: bool


class RuntimeSettings(StrictModel):
    deadline_seconds: float = Field(default=120.0, ge=1, le=600)
    status_timeout_seconds: float = Field(default=3.0, ge=0.1, le=10)
    retention_days: int = Field(default=30, ge=1, le=365)


class Settings(StrictModel):
    study_version: str = "GK-P1.2"
    ollama_url: str
    model: str = Field(min_length=1)
    embedding_model: str = Field(min_length=1)
    profile: str = Field(min_length=1)
    generation: GenerationSettings
    retrieval: RetrievalSettings
    policies: dict[str, Policy]
    default_policy: str
    runtime: RuntimeSettings = Field(default_factory=RuntimeSettings)

    @field_validator("ollama_url")
    @classmethod
    def local_endpoint(cls, value):
        url = urlsplit(value)
        try:
            url.port
        except ValueError as exc:
            raise ValueError("Porta local invalida") from exc
        if (url.scheme != "http" or url.hostname not in {"127.0.0.1", "localhost", "::1"}
                or url.username or url.password or url.query or url.fragment or url.path not in {"", "/"}):
            raise ValueError("O Ollama deve usar um endereco HTTP local sem credenciais.")
        return value.rstrip("/")

    @model_validator(mode="after")
    def known_default(self):
        if self.default_policy not in self.policies:
            raise ValueError("A politica padrao deve existir em policies.")
        if self.study_version.startswith("GK-P2") and (
                set(self.policies) != {"comum"} or self.default_policy != "comum"
                or not self.policies["comum"].allow_educational_predation):
            raise ValueError("GK-P2 requer uma única regra comum que permita predação educativa.")
        return self
