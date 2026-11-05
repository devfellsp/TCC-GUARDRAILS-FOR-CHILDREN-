"""Verificacoes da ampliacao por materia, sem inferencias reais."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]
VERSION = ROOT / "poc/versions/GK-P2.6-dev"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, VERSION / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


names = ("channels", "settings", "privacy", "response_styles", "vocabulary", "guardkids")
previous = {name: sys.modules.get(name) for name in names}
try:
    for name in names:
        load(name, name + ".py")
    g = sys.modules["guardkids"]
    app_module = load("school_subjects_app", "app.py")
finally:
    for name, value in previous.items():
        if value is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = value


@pytest.fixture(scope="module")
def corpus():
    return g.extract_corpus(g.config())[0]


def test_every_subject_has_traceable_sources_and_examples(corpus):
    assert len(g.CHANNELS) == 10
    assert {c["channel"] for c in corpus} == set(g.CHANNELS)
    assert len({c["id"] for c in corpus}) == len(corpus)
    assert all(len(info["examples"]) == 3 for info in g.CHANNELS.values())
    assert len({c["file"] for c in corpus if c["file"].endswith(".pdf")}) == 6
    assert all(c["pdf_page"] and c["printed_page"] for c in corpus if c["file"].endswith(".pdf"))


@pytest.mark.parametrize("channel", list(g.CHANNELS))
def test_search_never_uses_other_subjects_even_when_they_rank_higher(channel, monkeypatch):
    chunks = [
        dict(id="foreign", text="Texto de outra materia.", channel="outra"),
        dict(id="correct", text="Texto da materia escolhida.", channel=channel),
    ]
    vectors = np.array([[1.0, 0.0], [0.8, 0.6]])
    monkeypatch.setattr(g, "load_index", lambda *a: (dict(chunks=chunks), vectors, "mock"))
    class Client:
        def identities(self): return {}
        def check_budget(self): pass
        def embed(self, texts): return np.array([[1.0, 0.0]])
    chosen, _ = g.retrieve("pergunta ficticia", g.config(), Client(), channel)
    assert [c["id"] for c in chosen] == ["correct"]


@pytest.mark.parametrize("channel", list(g.CHANNELS))
def test_private_data_is_protected_in_every_subject(channel, tmp_path, monkeypatch):
    cfg = g.config()
    monkeypatch.setattr(g, "BASE", tmp_path)
    monkeypatch.setattr(g, "config", lambda: cfg)
    monkeypatch.setattr(g, "save_snapshot", lambda cfg: "ficticio")
    monkeypatch.setattr(g.Ollama, "request", lambda *a, **kw: pytest.fail("Dados pessoais nao devem chegar ao modelo"))
    result = g.run_question("Meu CPF ficticio e 123.456.789-09.", channel=channel)
    assert result["valid"] and result["action"] == "safe_guidance"
    saved = g.read_json(tmp_path / "runs" / (result["id"] + ".json"))
    assert saved["question"] == "[texto omitido pelo modo de privacidade]"


def test_api_lists_and_accepts_all_subjects_but_rejects_unknown_subject():
    with TestClient(app_module.app, base_url="http://127.0.0.1") as client:
        response = client.get("/api/channels")
        assert response.status_code == 200
        assert set(response.json()) == set(g.CHANNELS)
        for channel in g.CHANNELS:
            assert app_module.Question(question="Pergunta ficticia", channel=channel).channel == channel
        assert client.post("/api/ask", json=dict(question="Ficticia", channel="../../arquivo")).status_code == 422
        assert client.get("/").headers["cache-control"] == "no-store"
        assert client.post("/api/ask", headers={"Origin": "https://example.invalid"}, json=dict(question="Ficticia")).status_code == 403


def test_generation_cannot_cite_foreign_or_invented_sources():
    source = dict(id="math", text="Na leitura das fracoes, lemos o numerador normalmente.")
    draft = g.Draft(supported=True, claims=[g.Claim(text=source["text"], evidence=[g.Evidence(source_id="foreign")])])
    assert g.assemble_draft(draft, [source], "padrao") is None


def test_tampered_selection_is_rejected(tmp_path, monkeypatch):
    manifest = g.read_json(VERSION / "corpus_manifest.json")
    manifest["sources"][-1]["source_sha256"] = "0" * 64
    (tmp_path / "corpus_manifest.json").write_text(__import__("json").dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(g, "BASE", tmp_path)
    with pytest.raises(ValueError, match="difere do manifesto"):
        g.extract_corpus(g.config() if (tmp_path / "config.json").exists() else g.Settings.model_validate(g.read_json(VERSION / "config.json")).model_dump())


def test_launcher_restores_missing_active_index_without_model_inference(tmp_path, monkeypatch):
    import shutil
    for name in ("config.json", "corpus_manifest.json"):
        shutil.copyfile(VERSION / name, tmp_path / name)
    shutil.copytree(VERSION / "indice_preservado", tmp_path / "indice_preservado")
    monkeypatch.setattr(g, "BASE", tmp_path)
    monkeypatch.setitem(sys.modules, "guardkids", g)
    restore_module = load("restore_index", "restore_index.py")
    monkeypatch.setitem(sys.modules, "restore_index", restore_module)
    launcher = load("school_subjects_launcher", "launch.py")
    monkeypatch.setattr(launcher, "BASE", tmp_path)
    cfg = g.config()
    monkeypatch.setattr(launcher, "ensure_ollama", lambda: dict(models=[dict(name=cfg["model"]), dict(name=cfg["embedding_model"])]))
    monkeypatch.setattr(g.Ollama, "request", lambda *a, **kw: pytest.fail("Restauracao nao pode inferir ou reconstruir embeddings"))
    assert not (tmp_path / "data/current.json").exists()
    launcher.prepare()
    assert g.load_index(cfg)[2] == g.read_json(tmp_path / "indice_preservado/current.json")["id"]

