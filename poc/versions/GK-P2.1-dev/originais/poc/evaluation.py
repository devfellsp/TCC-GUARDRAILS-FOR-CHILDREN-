"""Protocolo rastreavel: desenvolvimento executavel, avaliacao final condicionada a revisao humana."""
import argparse
import csv
import hashlib
import json
import random
import statistics
from datetime import datetime, timezone
from pathlib import Path

import guardkids as g

STUDY = g.ROOT / "avaliacao"


def require_legacy_design():
    if set(g.config()["policies"]) != {"referencia", "ajustada"}:
        raise ValueError("Protocolo anterior de Ciências arquivado. Use run_development.py para o desenho atual de regra comum e estilos.")


def schedule(cases, repetitions=2, seed=20261103):
    rng = random.Random(seed)
    result = []
    for repeat in range(1, repetitions + 1):
        order = list(cases)
        rng.shuffle(order)
        for i, case in enumerate(order):
            # O primeiro tratamento alterna entre casos e a repeticao seguinte troca a ordem.
            first = (int(hashlib.sha256(case["case_id"].encode()).hexdigest(), 16) + repeat) % 2
            policies = ["referencia", "ajustada"] if first == 0 else ["ajustada", "referencia"]
            for policy in policies:
                key = f"{seed}|{case['case_id']}|{policy}|{repeat}"
                result.append({"observation_id": hashlib.sha256(key.encode()).hexdigest()[:16],
                               "case_id": case["case_id"], "family_id": case["family_id"], "policy": policy,
                               "repetition": repeat, "order": len(result) + 1})
    return result


def source_manifest():
    paths = [*g.BASE.glob("*.py"), *g.BASE.glob("tests/*.py"), *g.BASE.glob("prompts/*.txt"),
             g.BASE / "config.json", g.BASE / "corpus_manifest.json", g.BASE / "requirements-lock.txt",
             *g.BASE.glob("*cases.json"), *g.BASE.glob("corpus/*.txt"), STUDY / "protocolo.json", STUDY / "casos_avaliacao.json", STUDY / "RUBRICA.md",
             STUDY / "PROTOCOLO.md", STUDY / "corpus_referencia.json", STUDY / "referencia_para_revisao_humana.csv"]
    if (STUDY / "referencia_ratificada.json").exists():
        paths.append(STUDY / "referencia_ratificada.json")
    return {str(p.relative_to(g.ROOT)).replace("\\", "/"): g.digest(p.read_bytes()) for p in sorted(set(paths))}


def freeze():
    require_legacy_design()
    cfg = g.config()
    client = g.Ollama(cfg)
    models = client.identities()
    _, _, index_id = g.load_index(cfg, models)
    value = {"version": cfg["study_version"], "time_utc": datetime.now(timezone.utc).isoformat(),
             "sources": source_manifest(), "index_id": index_id,
             "model_digests": {key: models[key] for key in [cfg["model"], cfg["embedding_model"]]},
             "ollama_version": client.request("/api/version").get("version"), "snapshot": g.save_snapshot(cfg),
             "phase": "candidato_tecnico_TCC_I", "human_reference_status": g.read_json(STUDY / "protocolo.json")["human_reference_status"]}
    identifier = g.digest(value)
    g.atomic_json(STUDY / "congelamentos" / f"{identifier}.json", value)
    g.atomic_json(STUDY / "congelamento_ativo.json", {"id": identifier})
    return identifier, value


def verify_freeze():
    require_legacy_design()
    identifier = g.read_json(STUDY / "congelamento_ativo.json")["id"]
    frozen = g.read_json(STUDY / "congelamentos" / f"{identifier}.json")
    if g.digest(frozen) != identifier or frozen["sources"] != source_manifest():
        raise ValueError("Codigo, prompts, casos ou protocolo alterados: crie um novo congelamento")
    cfg = g.config()
    models = g.Ollama(cfg).identities()
    if any(models.get(k) != v for k, v in frozen["model_digests"].items()):
        raise ValueError("Modelo alterado")
    _, _, current_id = g.load_index(cfg, models)
    if current_id != frozen["index_id"]:
        raise ValueError("Indice alterado")
    return identifier, frozen


def development():
    identifier, frozen = verify_freeze()
    folder = STUDY / "evidencias" / ("desenvolvimento_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
    folder.mkdir(parents=True)
    g.atomic_json(folder / "congelamento.json", {"id": identifier, **frozen})
    rows = []
    cases = []
    for suite in ["development", "adversarial", "development_help"]:
        cases.extend(dict(c, suite=suite) for c in g.read_json(g.BASE / f"{suite}_cases.json"))
    for i, case in enumerate(cases):
        for policy in (["referencia", "ajustada"] if i % 2 == 0 else ["ajustada", "referencia"]):
            verify_freeze()
            run = g.run_question(case["question"], policy, case_id=case["id"], group=case["group"], split="development", synthetic=True)
            run.update(study_freeze=identifier, suite=case["suite"], human_review=None,
                       expected_treatment_assisted_IA=case["expected"])
            g.atomic_json(folder / "runs" / f"{run['id']}.json", run)
            snapshot_id = run.get("snapshot")
            if snapshot_id:
                target = folder / "snapshots" / f"{snapshot_id}.json"
                if not target.exists():
                    g.atomic_json(target, g.read_json(g.BASE / "runs/snapshots" / f"{snapshot_id}.json"))
            row = {"case_id": case["id"], "suite": case["suite"], "group": case["group"], "policy": policy,
                   "repetition": 1, "version": g.config()["study_version"], "freeze_id": identifier,
                   "question": case["question"], "expected_treatment_assisted_IA": case["expected"],
                   "answer": run["answer"], "action": run["action"], "valid": run["valid"],
                   "seconds": run["seconds"], "final_origin": run["final_origin"], "error": run.get("error", ""),
                   "run_id": run["id"], "human_review": "pendente"}
            rows.append(row)
            # Grava incrementalmente: uma interrupcao nao apaga execucoes ja concluidas.
            with (folder / "resultados.csv").open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
            print(json.dumps({k: row[k] for k in ["case_id", "policy", "action", "valid", "seconds"]}), flush=True)
    valid = [r for r in rows if r["valid"]]
    groups = {}
    for r in rows:
        key = r["policy"] + "/" + r["action"]
        groups[key] = groups.get(key, 0) + 1
    summary = {"kind": "desenvolvimento_sem_julgamento_humano", "questions": len(cases), "executions": len(rows),
               "valid": len(valid), "technical_losses": len(rows) - len(valid), "routes": groups,
               "seconds_min": min(r["seconds"] for r in rows), "seconds_median": statistics.median(r["seconds"] for r in rows),
               "seconds_max": max(r["seconds"] for r in rows), "freeze_id": identifier,
               "human_review": "pendente", "safety_rate": None, "educational_quality": None}
    g.atomic_json(folder / "resumo.json", summary)
    g.atomic_json(STUDY / "evidencias/desenvolvimento_ativo.json", {"folder": str(folder.relative_to(g.ROOT)).replace("\\", "/")})
    return summary


def ratify(path):
    require_legacy_design()
    cases = {c["case_id"]: c for c in g.read_json(STUDY / "casos_avaliacao.json")}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != len(cases) or {r["case_id"] for r in rows} != set(cases):
        raise ValueError("Referencia precisa cobrir todos os casos uma unica vez")
    for row in rows:
        case = cases[row["case_id"]]
        if row.get("confirmado") != "sim" or not all(row.get(k, "").strip() for k in ["avaliador_humano", "data", "justificativa"]):
            raise ValueError("Ratificacao humana incompleta")
        datetime.fromisoformat(row["data"])
        for key in ["question", "category", "expected_treatment"]:
            if row[key] != case[key]:
                raise ValueError("Corrija os casos antes de ratificar: " + key)
        expected_support = "" if case["corpus_support"] is None else str(case["corpus_support"])
        if row["corpus_support"] != expected_support or row["reference_ids"] != ";".join(case["reference_ids"]):
            raise ValueError("Apoio diverge dos casos; corrija e submeta novamente")
    g.atomic_json(STUDY / "referencia_ratificada.json", {"rows": rows, "source_sha256": g.digest(path.read_bytes()), "natureza": "humana_declarada"})
    protocol = g.read_json(STUDY / "protocolo.json")
    protocol.update(human_reference_status="confirmada", status="referencia ratificada; requer novo congelamento")
    g.atomic_json(STUDY / "protocolo.json", protocol)


def calibration():
    require_legacy_design()
    cfg = g.config(); client = g.Ollama(cfg)
    meta, vectors, identifier = g.load_index(cfg, client.identities())
    cases = [dict(c, suite=s) for s in ["development", "adversarial", "development_help"] for c in g.read_json(g.BASE / f"{s}_cases.json")]
    rows = []
    for case in cases:
        scores = vectors @ client.embed([case["question"]])[0]
        order = scores.argsort()[::-1][:3]
        rows.append({"case_id": case["id"], "suite": case["suite"], "question": case["question"],
                     "max_similarity": float(scores[order[0]]), "top3_ids": [meta["chunks"][int(i)]["id"] for i in order],
                     "passes": {str(t): bool(scores[order[0]] >= t) for t in [0.35, 0.45, 0.55]}})
    value = {"kind": "sondagem_de_recuperacao_desenvolvimento_sem_julgamento", "date_utc": datetime.now(timezone.utc).isoformat(),
             "index_id": identifier, "rows": rows, "thresholds": [0.35, 0.45, 0.55], "selected": 0.45,
             "passed_counts": {str(t): sum(r["passes"][str(t)] for r in rows) for t in [0.35, 0.45, 0.55]},
             "reason": "Referencia historica mantida; passagem nao demonstra apoio nem otimalidade"}
    g.atomic_json(STUDY / "evidencias/calibracao_desenvolvimento.json", value)
    return {k: v for k, v in value.items() if k != "rows"}


def evaluation():
    identifier, frozen = verify_freeze()
    protocol = g.read_json(STUDY / "protocolo.json")
    if frozen["human_reference_status"] != "confirmada" or not (STUDY / "referencia_ratificada.json").exists():
        raise ValueError("Avaliacao final nao liberada: ratifique referencias humanas e congele novamente")
    cases = {c["case_id"]: c for c in g.read_json(STUDY / "casos_avaliacao.json")}
    agenda = schedule(list(cases.values()), protocol["repetitions"], protocol["order_seed"])
    folder = STUDY / "evidencias" / ("avaliacao_final_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
    folder.mkdir(parents=True)
    g.atomic_json(folder / "agenda.json", agenda)
    g.atomic_json(folder / "congelamento.json", {"id": identifier, **frozen})
    rows = []
    for item in agenda:
        verify_freeze(); case = cases[item["case_id"]]
        run = g.run_question(case["question"], item["policy"], case_id=case["case_id"], group=case["group"], split="evaluation", synthetic=True)
        run.update(study_freeze=identifier, observation_id=item["observation_id"], repetition=item["repetition"], human_review=None)
        g.atomic_json(folder / "runs" / f"{run['id']}.json", run)
        if run.get("snapshot"):
            g.atomic_json(folder / "snapshots" / f"{run['snapshot']}.json", g.read_json(g.BASE / "runs/snapshots" / f"{run['snapshot']}.json"))
        rows.append({**item, "group": case["group"], "category": case["category"], "version": frozen["version"],
                     "question": case["question"], "answer": run["answer"], "action": run["action"], "valid": run["valid"],
                     "seconds": run["seconds"], "error": run.get("error", ""), "final_origin": run["final_origin"], "run_id": run["id"]})
        with (folder / "resultados.csv").open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
        print(item["observation_id"], run["action"], flush=True)
    g.atomic_json(STUDY / "evidencias/avaliacao_final_ativa.json", {"folder": str(folder.relative_to(g.ROOT)).replace("\\", "/")})
    return {"executions": len(rows), "folder": str(folder), "human_review": "pendente"}


def metric_summary(rows):
    from metrics import summary
    return summary(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["freeze", "development", "calibration", "ratify", "evaluation", "metrics"])
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()
    if args.command == "freeze":
        identifier, _ = freeze(); print(identifier)
    elif args.command == "development":
        print(json.dumps(development(), ensure_ascii=False, indent=2))
    elif args.command == "evaluation":
        print(json.dumps(evaluation(), ensure_ascii=False, indent=2))
    elif args.command == "calibration":
        print(json.dumps(calibration(), ensure_ascii=False, indent=2))
    elif args.command == "ratify" and args.csv:
        ratify(args.csv); print("Referencias ratificadas; congele novamente antes de executar")
    elif args.csv:
        with args.csv.open(encoding="utf-8-sig", newline="") as stream:
            print(json.dumps(metric_summary(list(csv.DictReader(stream))), ensure_ascii=False, indent=2))
    else:
        parser.error("Informe --csv")


if __name__ == "__main__":
    main()
