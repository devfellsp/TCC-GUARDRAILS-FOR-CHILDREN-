"""Audita as correções sem inferência ou alteração de evidências."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "poc/versions/GK-P2.5-dev"
FOLDER = ROOT / "avaliacao/evidencias/correcoes_GK_P2_5_dev_20261105"
sys.path.insert(0, str(BASE))
import guardkids as g
import run_expansion as runner


def verify():
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    plan = g.read_json(FOLDER / "plano.json")
    content = {k: v for k, v in plan.items() if k != "plan_id"}
    require(g.digest(content) == plan["plan_id"], "Plano alterado")
    require(runner.fingerprint() == plan["inputs"], "Arquivos da execução alterados")
    snapshot_path = FOLDER / "snapshots" / f"{plan['snapshot']}.json"
    snapshot = g.read_json(snapshot_path)
    require(g.digest(snapshot) == plan["snapshot"], "Snapshot alterado")
    require(snapshot_path.read_bytes() == (BASE / "runs/snapshots" / snapshot_path.name).read_bytes(), "Snapshot original divergente")
    meta, vectors, index_id = g.load_index(g.config())
    require(index_id == plan["index_id"] == snapshot["index"]["id"], "Índice divergente")
    require(meta == snapshot["index"]["metadata"], "Metadados do snapshot divergentes")
    require(g.digest(vectors.tobytes()) == meta["vector_hash"], "Vetores alterados")
    require(g.read_json(BASE / "indice_preservado/current.json")["id"] == index_id, "Ponteiro preservado divergente")
    for filename in ("chunks.json", "index.npz"):
        require((BASE / "indice_preservado" / index_id / filename).read_bytes() ==
                (BASE / "data/indices" / index_id / filename).read_bytes(), "Cópia do índice divergente")
    with (FOLDER / "resultados.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == len(plan["agenda"]) == plan["planned_attempts"], "Lote incompleto")
    require(len({r["run_id"] for r in rows}) == len(rows), "Tentativa duplicada")
    require(len(list((FOLDER / "runs").glob("*.json"))) == len(rows), "Arquivos extras ou ausentes")
    retrieved_reference = cited_reference = educational = 0
    for scheduled, row in zip(plan["agenda"], rows):
        for key, value in scheduled.items():
            require(str(value) == row[key], f"Agenda divergente: {key}")
        raw_path = FOLDER / "runs" / f"{row['run_id']}.json"
        raw = g.read_json(raw_path)
        require(raw_path.read_bytes() == (BASE / "runs" / raw_path.name).read_bytes(), "Log original divergente")
        for key in ("case_id", "question", "channel", "response_style", "group", "policy", "action", "answer", "snapshot"):
            require(row[key] == raw[key], f"Registro divergente: {key}")
        require(raw["configuration"] == snapshot["configuration"], "Configuração divergente")
        require(raw["snapshot"] == plan["snapshot"], "Identidade divergente")
        # Rotas que encerram antes da busca não possuem index_hash no registro.
        require(raw.get("index_hash", index_id) == index_id, "Índice utilizado divergente")
        require(not raw["retrieved"] or raw.get("index_hash") == index_id, "Busca sem identidade de índice")
        require(raw["synthetic"] is True and raw["split"] == "development", "Registro fora do desenvolvimento fictício")
        require(row["valid"] == str(raw["valid"]) and row["error"] == raw.get("error", ""), "Perda técnica divergente")
        require(all(not value for key, value in row.items() if key.startswith("human_")), "Campo humano preenchido")
        require(all(c["channel"] == row["channel"] for c in raw["retrieved"]), "Fonte de outro chat")
        found = {c["id"] for c in raw["retrieved"]}
        cited = (raw.get("generated") or {}).get("source_ids", [])
        require(set(cited) <= found, "Citação inexistente ou não recuperada")
        require(row["retrieved_ids"] == ";".join(c["id"] for c in raw["retrieved"]), "Lista de recuperação divergente")
        require(row["cited_ids"] == ";".join(cited), "Lista de citação divergente")
        if row["reference_ids"]:
            educational += 1
            reference = set(row["reference_ids"].split(";"))
            retrieved_reference += int(reference <= found)
            cited_reference += int(reference <= set(cited))
    previous = g.read_json(BASE / "preservacao_anterior.json")
    require(all((ROOT / name).is_file() and hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected
                for name, expected in previous["protected_files"].items()), "Versão GK-P2.2 alterada")
    for row in rows:
        raw = g.read_json(FOLDER / "runs" / f"{row['run_id']}.json")
        if raw["action"] == "allow":
            proposal = g.Draft.model_validate(raw["released_draft"])
            if raw["final_origin"] == "extractive_fallback":
                require(proposal == g.extractive_draft(raw["retrieved"]), "Alternativa literal divergente")
                require(len(raw["candidate_checks"]) == 2 and raw["candidate_checks"][0].get("rejected_by"),
                        "Rascunho inicial não preservado")
            assembled = g.assemble_draft(proposal, raw["retrieved"], raw["response_style"])
            require(assembled is not None and assembled.answer == raw["answer"], "Resposta sem ancoragem")
            require(raw["claim_evidence"] == g.claim_evidence(proposal, raw["retrieved"]), "Evidência literal divergente")
            audit_data = dict(raw["grounding_guard"])
            require(audit_data.pop("supported") is True, "Resposta sem aprovação")
            require(g.grounding_accepts(g.Grounding.model_validate(audit_data), proposal), "Auditoria incompleta")
    baseline = g.read_json(ROOT / "poc/versions/GK-P2.1-dev/preservacao.json")
    changed = [name for name, expected in baseline["protected_files"].items()
               if not (ROOT / name).is_file() or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected]
    require(not changed, f"Arquivos protegidos alterados: {changed}")
    summary = g.read_json(FOLDER / "resumo.json")
    require(summary["routes"] == dict(Counter(r["action"] for r in rows)), "Resumo de rotas divergente")
    require(summary["technical_losses"] == sum(r["valid"] != "True" for r in rows), "Resumo de perdas divergente")
    guard_plan = g.read_json(FOLDER / "guard_checks/plan.json")
    guard_content = {k: v for k, v in guard_plan.items() if k != "plan_id"}
    require(g.digest(guard_content) == guard_plan["plan_id"], "Plano diagnóstico alterado")
    require(guard_plan["snapshot"] == plan["snapshot"] and guard_plan["inputs"] == plan["inputs"],
            "Versão do diagnóstico divergente")
    guards = g.read_json(FOLDER / "guard_checks/results.json")
    require(guards["snapshot"] == plan["snapshot"] and len(guards["results"]) == len(guard_plan["cases"]),
            "Diagnóstico incompleto")
    require(all(r["valid"] and r["accepted"] == r["expected_acceptance_proposed"] for r in guards["results"]),
            "Diagnóstico divergente da referência proposta")
    return {"version": plan["version"], "verified_attempts": len(rows), "index_id": index_id,
            "snapshot": plan["snapshot"], "educational_attempts": educational,
            "proposed_reference_retrieved": retrieved_reference, "proposed_reference_cited": cited_reference,
            "cross_channel_sources": 0, "unretrieved_citations": 0, "filled_human_fields": 0,
            "baseline_files_checked": len(baseline["protected_files"]), "baseline_files_changed": changed,
            "diagnostic_cases": len(guards["results"]),
            "extractive_answers": sum(g.read_json(FOLDER / "runs" / f"{r['run_id']}.json")["final_origin"] == "extractive_fallback" for r in rows),
            "note": "Integridade e correspondência de IDs; não certifica sustentação semântica ou eficácia."}


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=True, indent=2))
