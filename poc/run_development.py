"""Piloto funcional; não calcula eficácia e não substitui julgamento humano."""
import argparse
import csv
import json
from datetime import datetime

from guardkids import BASE, read_json, run_question

parser = argparse.ArgumentParser()
parser.add_argument("--policies", nargs="+", default=["ajustada"], choices=["ajustada", "referencia"])
args = parser.parse_args()
rows = []
for case in read_json(BASE / "development_cases.json"):
    for policy in args.policies:
        r = run_question(case["question"], policy, case["id"], case["group"], "development")
        rows.append({"case_id": case["id"], "group": case["group"], "question": case["question"], "policy": policy,
                     "expected_adjusted": case["expected"], "observed": r["action"], "valid": r["valid"],
                     "seconds": r["seconds"], "answer": r["answer"], "run_id": r["id"],
                     "human_inadequate": "", "human_undue_block": "", "human_correctness": "",
                     "human_relevance": "", "human_clarity": "", "human_notes": ""})
        print(json.dumps({"case": case["id"], "policy": policy, "action": r["action"], "seconds": r["seconds"], "valid": r["valid"]}, ensure_ascii=False), flush=True)
path = BASE / "runs" / f"development_{datetime.now():%Y%m%d_%H%M%S}.csv"
with path.open("w", encoding="utf-8-sig", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f"Arquivo para revisão humana: {path}")
