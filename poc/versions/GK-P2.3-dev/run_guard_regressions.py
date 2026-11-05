"""Reavalia saídas anteriores de desenvolvimento, sem regenerar ou substituir o lote."""
import argparse
import csv
import json

import guardkids as g
from run_expansion import fingerprint, FOLDER

OLD = g.ROOT / "avaliacao/evidencias/ampliacao_GK_P2_2_dev_20261105"
TARGET = FOLDER / "guard_checks"
SELECTION = [
    ("exp22-h01", "passo_a_passo", False),
    ("exp22-h02", "passo_a_passo", False),
    ("exp22-h04", "passo_a_passo", False),
    ("exp22-g03", "padrao", False),
    ("exp22-h03", "padrao", False),
    ("exp22-g04", "padrao", False),
    ("exp22-h04", "padrao", True),
    ("exp22-h05", "padrao", True),
]


def plan():
    with (OLD / "resultados.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    cases = []
    for case_id, style, expected in SELECTION:
        row = next(r for r in rows if r["case_id"] == case_id and r["response_style"] == style)
        raw_path = OLD / "runs" / f"{row['run_id']}.json"
        raw = g.read_json(raw_path)
        sources = [c for c in raw["retrieved"] if c["id"] in raw["generated"]["source_ids"]]
        proposal = g.Draft(supported=True, claims=[g.Claim(text=raw["answer"], evidence=[
            g.Evidence(source_id=c["id"], quote=c["text"]) for c in sources])])
        cases.append(dict(case_id=case_id, response_style=style, question=raw["question"],
                          prior_run_id=row["run_id"], prior_sha256=g.digest(raw_path.read_bytes()),
                          draft=proposal.model_dump(), sources=sources, expected_acceptance_proposed=expected))
    value = dict(version=g.config()["study_version"], snapshot=g.save_snapshot(g.config()), inputs=fingerprint(),
                 cases=cases, human_review="pendente", note="Regressão diagnóstica de saídas de desenvolvimento conhecidas, não avaliação cega ou final.")
    value["plan_id"] = g.digest(value)
    if (TARGET / "results.json").exists():
        raise ValueError("Regressão já executada")
    if (TARGET / "plan.json").exists() and g.read_json(TARGET / "plan.json") != value:
        raise ValueError("Plano anterior divergente")
    g.atomic_json(TARGET / "plan.json", value)


def execute():
    value = g.read_json(TARGET / "plan.json")
    identity = value.pop("plan_id")
    if g.digest(value) != identity or fingerprint() != value["inputs"]:
        raise ValueError("Plano ou arquivos alterados")
    if (TARGET / "results.json").exists():
        raise ValueError("Não repetir seletivamente")
    results = []
    for case in value["cases"]:
        if fingerprint() != value["inputs"] or g.save_snapshot(g.config()) != value["snapshot"]:
            raise ValueError("Implementação mudou")
        row = dict(case_id=case["case_id"], response_style=case["response_style"],
                   expected_acceptance_proposed=case["expected_acceptance_proposed"], accepted=None, valid=False)
        client = g.Ollama(g.config())
        try:
            draft = g.Draft.model_validate(case["draft"])
            generated = g.assemble_draft(draft, case["sources"], "padrao")
            if generated is None:
                raise ValueError("Entrada da regressão sem evidência literal")
            audit = client.structured("grounding.txt", dict(question=case["question"], answer=generated.answer,
                claims=[dict(number=i, **c.model_dump()) for i, c in enumerate(draft.claims, 1)],
                sources=case["sources"]), g.Grounding, "grounding_guard")
            row.update(valid=True, accepted=g.grounding_accepts(audit, draft), audit=audit.model_dump(),
                       model_digests=client.identities())
        except Exception as exc:
            row["error"] = type(exc).__name__
        row["calls"] = client.calls
        results.append(row)
        g.atomic_json(TARGET / "results.json", dict(snapshot=value["snapshot"], results=results,
                      human_review="pendente", note="Verificações automatizadas, sem reexecução seletiva."))
        print(json.dumps(row, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "run"))
    args = parser.parse_args()
    plan() if args.command == "plan" else execute()
