"""Desenvolvimento pareado de linguagem com regra de proteção comum.

--plan prepara a agenda sem iniciar serviços ou chamar o modelo.
"""
import argparse
import csv
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from guardkids import BASE, atomic_json, config, digest, read_json, run_question, save_snapshot
from response_styles import RESPONSE_STYLES


def schedule(cases, styles=None, seed=20261104):
    styles = list(RESPONSE_STYLES) if styles is None else list(styles)
    if not styles or len(styles) != len(set(styles)) or any(s not in RESPONSE_STYLES for s in styles):
        raise ValueError("Estilos inválidos")
    if not cases or len({c["id"] for c in cases}) != len(cases):
        raise ValueError("Casos vazios ou identificadores duplicados")
    ordered = list(cases)
    random.Random(seed).shuffle(ordered)
    rows = []
    for index, case in enumerate(ordered):
        for style in (styles if index % 2 == 0 else list(reversed(styles))):
            rows.append({"order":len(rows) + 1, "case_id":case["id"],
                         "channel":case.get("channel", "ciencias"), "group":case["group"],
                         "question":case["question"], "policy":"comum", "response_style":style,
                         "expected_action_proposed":case["expected"], "repetition":1})
    return rows


def execute(agenda, folder, suite):
    """Persiste cada tentativa; erro de gravação interrompe o lote."""
    initial_snapshot = save_snapshot(config())
    rows = []
    for item in agenda:
        if save_snapshot(config()) != initial_snapshot:
            raise ValueError("Configuração, fontes ou implementação mudaram durante o lote")
        r = run_question(item["question"], "comum", item["case_id"], item["group"],
                         "development", synthetic=True, channel=item["channel"], response_style=item["response_style"])
        row = {**item, "suite":suite, "observed":r["action"], "valid":r["valid"],
               "seconds":r["seconds"], "answer":r["answer"], "run_id":r["id"],
               "snapshot":r.get("snapshot", ""), "error":r.get("error", ""),
               "human_safety":"", "human_undue_refusal":"", "human_correctness":"",
               "human_source_support":"", "human_clarity":"", "human_example_quality":"",
               "human_notes":"", "human_evaluator":"", "human_date":""}
        rows.append(row)
        with (folder / "resultados.csv").open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(row))
            writer.writeheader()
            writer.writerows(rows)
        print(json.dumps({k:row[k] for k in ["case_id", "response_style", "observed", "valid"]}), flush=True)
    atomic_json(folder / "resumo.json", {"executions":len(rows), "technical_losses":sum(not r["valid"] for r in rows),
                "snapshot":initial_snapshot, "human_review":"pendente", "efficacy":None})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", default="multichat", choices=["development", "adversarial", "multichat"])
    parser.add_argument("--response-style", choices=list(RESPONSE_STYLES), help="Omitir para comparar os dois estilos")
    parser.add_argument("--plan", action="store_true", help="Preparar agenda sem chamar o modelo")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cfg = config()
    if set(cfg["policies"]) != {"comum"}:
        parser.error("Este executor requer a regra comum")
    cases = read_json(BASE / f"{args.suite}_cases.json")
    agenda = schedule(cases, [args.response_style] if args.response_style else None)
    folder = args.output or BASE / "runs" / ("multichat_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(parents=True, exist_ok=True)
    plan = {"version":cfg["study_version"], "phase":"development", "suite":args.suite,
            "status":"planejado; não executado", "questions":len(cases), "planned_executions":len(agenda),
            "seed":20261104, "case_hash":digest(cases), "configuration_hash":digest(cfg),
            "styles_hash":digest(RESPONSE_STYLES), "human_reference":"proposta assistida por IA; pendente de revisão",
            "agenda":agenda}
    if (folder / "agenda.json").exists():
        parser.error("A pasta já possui agenda; use uma nova pasta para preservar a evidência")
    atomic_json(folder / "agenda.json", plan)
    print(f"Agenda: {len(agenda)} tentativas sobre {len(cases)} perguntas. {folder}")
    if not args.plan:
        execute(agenda, folder, args.suite)


if __name__ == "__main__":
    main()
