"""Exportacao explicitamente sintetica e indicadores condicionados a julgamento humano."""
import argparse
import csv
import json
import os
import re
import uuid
import zipfile
from pathlib import Path

import guardkids as g


def export_experiment(run_ids, output):
    if not run_ids:
        raise ValueError("Selecione ao menos uma execucao sintetica")
    records, snapshots = [], {}
    for identifier in run_ids:
        if not re.fullmatch(r"[0-9a-f]{32}", identifier):
            raise ValueError("ID de execucao invalido")
        record = g.read_json(g.BASE / "runs" / f"{identifier}.json")
        if record.get("id") != identifier:
            raise ValueError("ID do registro divergente")
        if record.get("synthetic") is not True or record.get("logging_mode") != "synthetic":
            raise ValueError("A exportacao aceita apenas execucoes explicitamente ficticias")
        snapshot_id = record.get("snapshot", "")
        if not re.fullmatch(r"[0-9a-f]{64}", snapshot_id):
            raise ValueError("Snapshot ausente")
        snapshot = g.read_json(g.BASE / "runs/snapshots" / f"{snapshot_id}.json")
        if g.digest(snapshot) != snapshot_id:
            raise ValueError("Snapshot alterado")
        snapshots[snapshot_id] = snapshot
        records.append(record)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(f".{output.name}.{uuid.uuid4().hex}.tmp")
    try:
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as archive:
            for record in records:
                archive.writestr(f"runs/{record['id']}.json", json.dumps(record, ensure_ascii=False, indent=2))
            for key, value in snapshots.items():
                archive.writestr(f"snapshots/{key}.json", json.dumps(value, ensure_ascii=False, indent=2))
            archive.writestr("README.txt", "Dados declarados ficticios pelo executor. Snapshots incluem codigo, prompts, configuracao, versoes e indice quando disponivel. Pesos de modelos e PDFs nao incluidos. Julgamentos humanos nao sao inferidos das rotas. Revise direitos dos trechos antes de redistribuir.")
        os.replace(temp, output)
    finally:
        temp.unlink(missing_ok=True)
    return output


def summarize(rows):
    """Nunca converte a decisao do guardrail em verdade de referencia."""
    result = {}
    for policy in sorted({r["policy"] for r in rows}):
        subset = [r for r in rows if r["policy"] == policy]
        valid = [r for r in subset if str(r["valid"]).lower() == "true"]
        judged = [r for r in valid if r.get("human_inadequate") in {"0", "1"}
                  and r.get("human_evaluator", "").strip() and r.get("human_date", "").strip()
                  and r.get("human_notes", "").strip()]
        result[policy] = {"executions": len(subset), "technical_losses": len(subset) - len(valid),
                          "content_judged": len(judged), "content_pending": len(valid) - len(judged),
                          "T_RI": None if len(judged) != len(valid) or not valid else {
                              "numerator": sum(int(r["human_inadequate"]) for r in judged),
                              "denominator": len(judged),
                              "percent": 100 * sum(int(r["human_inadequate"]) for r in judged) / len(judged)}}
    return result


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export")
    export.add_argument("--run-ids", nargs="+", required=True)
    export.add_argument("--output", type=Path, required=True)
    summary = sub.add_parser("summary")
    summary.add_argument("csv", type=Path)
    args = parser.parse_args()
    if args.command == "export":
        print(export_experiment(args.run_ids, args.output))
    else:
        with args.csv.open(encoding="utf-8-sig", newline="") as stream:
            print(json.dumps(summarize(list(csv.DictReader(stream))), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
