"""Plano e lote fictício exclusivos da ampliação; não lê nem executa casos finais."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import random

import guardkids as g

FOLDER = g.ROOT / "avaliacao/evidencias/correcoes_GK_P2_4_dev_20261105"


def fingerprint():
    paths = [*g.BASE.glob("*.py"), *g.BASE.glob("*.cmd"), *g.BASE.glob("*.txt"),
             *g.BASE.glob("prompts/*.txt"), *g.BASE.glob("web/*.html"),
             *[g.BASE / n for n in ("config.json", "corpus_manifest.json", "development_cases.json", "recortes_selecionados.json")]]
    return {p.relative_to(g.BASE).as_posix(): g.digest(p.read_bytes()) for p in sorted(paths)}


def schedule(cases):
    ordered = list(cases)
    random.Random(20261105).shuffle(ordered)
    rows = []
    for i, case in enumerate(ordered):
        for style in (("padrao", "passo_a_passo") if i % 2 == 0 else ("passo_a_passo", "padrao")):
            rows.append({"order": len(rows) + 1, "case_id": case["id"], "channel": case["channel"],
                         "group": case["group"], "question": case["question"], "policy": "comum",
                         "response_style": style, "expected_action_proposed": case["expected_action_proposed"],
                         "reference_ids": ";".join(case["reference_ids"]), "repetition": 1})
    return rows


def plan(folder=FOLDER):
    if (folder / "resultados.csv").exists():
        raise ValueError("Lote já possui tentativas; não substituir nem repetir")
    cfg = g.config()
    assert cfg["study_version"] == "GK-P2.4-dev"
    chunks, _, _ = g.extract_corpus(cfg)
    cases = g.read_json(g.BASE / "development_cases.json")
    for case in cases:
        if case["synthetic"] is not True:
            raise ValueError("Apenas perguntas fictícias")
        for identifier in case["reference_ids"]:
            if not any(c["id"] == identifier and c["channel"] == case["channel"] for c in chunks):
                raise ValueError("Referência proposta ausente do respectivo chat")
    meta, _, index_id = g.load_index(cfg)
    value = {"version": cfg["study_version"], "phase": "development", "seed": 20261105,
             "questions": len(cases), "planned_attempts": len(cases) * 2,
             "snapshot": g.save_snapshot(cfg), "index_id": index_id,
             "chunks_by_channel": dict(Counter(c["channel"] for c in chunks)),
             "embedding_digest": meta["embedding_digest"], "inputs": fingerprint(), "agenda": schedule(cases),
             "human_review": "pendente", "efficacy": None,
             "note": "Planejamento anterior às tentativas; sem casos reservados e sem repetição seletiva."}
    value["plan_id"] = g.digest(value)
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "plano.json"
    if target.exists() and g.read_json(target) != value:
        raise ValueError("Plano anterior divergente")
    if not target.exists():
        g.atomic_json(target, value)
    return value


def write_rows(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def execute(folder=FOLDER):
    value = g.read_json(folder / "plano.json")
    identifier = value.pop("plan_id")
    if g.digest(value) != identifier or fingerprint() != value["inputs"]:
        raise ValueError("Plano ou implementação alterados")
    if (folder / "resultados.csv").exists():
        raise ValueError("Lote já iniciado; não repetir tentativas")
    rows = []
    for item in value["agenda"]:
        if fingerprint() != value["inputs"] or g.save_snapshot(g.config()) != value["snapshot"]:
            raise ValueError("Versão mudou durante o lote")
        record = g.run_question(item["question"], "comum", item["case_id"], item["group"], "development",
                                synthetic=True, channel=item["channel"], response_style=item["response_style"])
        if record.get("snapshot") != value["snapshot"]:
            raise ValueError("Snapshot da tentativa diverge do plano")
        row = {**item, "run_id": record["id"], "snapshot": record["snapshot"], "valid": record["valid"],
               "action": record["action"], "answer": record["answer"], "seconds": record["seconds"],
               "retrieved_ids": ";".join(c["id"] for c in record["retrieved"]),
               "cited_ids": ";".join((record.get("generated") or {}).get("source_ids", [])),
               "error": record.get("error", ""), "human_safety": "", "human_correctness": "",
               "human_source_support": "", "human_clarity": "", "human_reviewer": "", "human_date": "", "human_notes": ""}
        rows.append(row)
        write_rows(folder / "resultados.csv", rows)
        # Evidência do lote fora da pasta de logs ignorada, com bytes originais.
        original = g.BASE / "runs" / f"{record['id']}.json"
        target = folder / "runs" / original.name
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(original.read_bytes())
        snapshot = g.BASE / "runs/snapshots" / f"{value['snapshot']}.json"
        target = folder / "snapshots" / snapshot.name
        target.parent.mkdir(exist_ok=True)
        if not target.exists():
            target.write_bytes(snapshot.read_bytes())
        g.atomic_json(folder / "resumo.json", {"version": value["version"], "planned_attempts": value["planned_attempts"],
            "executed_attempts": len(rows), "questions": value["questions"], "snapshot": value["snapshot"],
            "index_id": value["index_id"], "technical_losses": sum(not r["valid"] for r in rows),
            "routes": dict(Counter(r["action"] for r in rows)),
            "route_agreement_with_proposed_reference": sum(r["action"] == r["expected_action_proposed"] for r in rows),
            "human_review": "pendente", "efficacy": None,
            "note": "Contagens técnicas em desenvolvimento; não equivalem a adequação de conteúdo."})
        print(json.dumps({k: row[k] for k in ("order", "case_id", "response_style", "action", "valid")}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "run"))
    args = parser.parse_args()
    if args.command == "plan":
        print(json.dumps(plan(), ensure_ascii=True, indent=2))
    else:
        execute()
