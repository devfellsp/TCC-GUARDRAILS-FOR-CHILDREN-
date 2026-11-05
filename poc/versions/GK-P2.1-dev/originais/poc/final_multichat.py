"""Avaliação prospectiva de estilos: agenda, ratificação, congelamento e execução.

Nenhuma referência assistida por IA é aceita como assinatura humana automática.
"""
import argparse
import csv
import random
from datetime import date, datetime, timezone
from pathlib import Path

import guardkids as g

STUDY = g.ROOT / "avaliacao/final_multichat_v1"


def schedule(cases, seed=202611041):
    ordered = list(cases)
    random.Random(seed).shuffle(ordered)
    rows = []
    for i, case in enumerate(ordered):
        styles = ["padrao", "passo_a_passo"] if i % 2 == 0 else ["passo_a_passo", "padrao"]
        for style in styles:
            identifier = g.digest(f"{seed}|{case['id']}|{style}")[:24]
            rows.append({"observation_id":identifier, "order":len(rows)+1,
                         "case_id":case["id"], "family_id":case["family_id"], "channel":case["channel"],
                         "group":case["group"], "response_style":style, "policy":"comum", "repetition":1})
    secondary = set()
    # Alternar por chat e grupo evita confundir tipo de caso com estilo.
    channels = sorted({r["channel"] for r in rows})
    groups = sorted({r["group"] for r in rows})
    for family in sorted({r["family_id"] for r in rows}):
        members = [r for r in rows if r["family_id"] == family]
        channel, group = members[0]["channel"], members[0]["group"]
        position = channels.index(channel) + groups.index(group)
        style = "padrao" if position % 2 == 0 else "passo_a_passo"
        candidates = [r for r in members if r["response_style"] == style]
        secondary.add(min(candidates, key=lambda r:r["observation_id"])["observation_id"])
    for row in rows:
        row["secondary_review"] = row["observation_id"] in secondary
    return rows


def inputs():
    cases = g.read_json(STUDY / "casos.json")
    protocol = g.read_json(STUDY / "protocolo.json")
    if len(cases) != protocol["questions"] or len({c["id"] for c in cases}) != len(cases):
        raise ValueError("Cobertura ou identificadores inválidos")
    return cases, protocol


def ratify(path):
    cases, _ = inputs()
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    by_id = {c["id"]:c for c in cases}
    if len(rows) != len(cases) or {r["id"] for r in rows} != set(by_id):
        raise ValueError("Referência deve cobrir os 32 casos uma vez")
    for row in rows:
        case = by_id[row["id"]]
        for key in ["family_id", "channel", "group", "category", "question", "expected_action"]:
            if row[key] != case[key]:
                raise ValueError("Corrija casos e referências antes de ratificar: " + key)
        if row["reference_ids"] != ";".join(case["reference_ids"]):
            raise ValueError("Referências divergem dos casos")
        if row.get("human_confirmed") != "sim" or not all(row.get(k, "").strip() for k in ["human_reviewer", "human_date", "human_reason"]):
            raise ValueError("Ratificação humana incompleta; não preencher por IA")
        date.fromisoformat(row["human_date"])
    g.atomic_json(STUDY / "referencia_ratificada.json", {"case_hash":g.digest(cases),
                  "csv_hash":g.digest(Path(path).read_bytes()), "csv_file":str(Path(path).resolve()),
                  "rows":rows, "nature":"humana declarada; identidade não autenticada pelo programa"})


def require_human_reference():
    path = STUDY / "referencia_ratificada.json"
    if not path.exists():
        raise ValueError("Avaliação final não liberada: ratificação humana pendente")
    value = g.read_json(path)
    cases, _ = inputs()
    if value["case_hash"] != g.digest(cases) or value["csv_hash"] != g.digest(Path(value["csv_file"]).read_bytes()):
        raise ValueError("Referência alterada; ratifique novamente")
    return value


def source_hashes():
    files = [*g.BASE.glob("*.py"), *g.BASE.glob("prompts/*.txt"), *g.BASE.glob("web/*.html"),
             *g.BASE.glob("corpus/*.txt"), g.BASE/"config.json", g.BASE/"corpus_manifest.json",
             g.BASE/"requirements-lock.txt", STUDY/"casos.json", STUDY/"protocolo.json", STUDY/"README.md",
             STUDY/"referencia_ratificada.json"]
    return {str(p.relative_to(g.ROOT)):g.digest(p.read_bytes()) for p in sorted(files)}


def freeze():
    require_human_reference()
    cfg = g.config()
    if set(cfg["policies"]) != {"comum"}:
        raise ValueError("Regra comum obrigatória")
    models = g.Ollama(cfg).identities()
    _, _, index_id = g.load_index(cfg, models)
    value = {"sources":source_hashes(), "models":models, "index_id":index_id,
             "snapshot":g.save_snapshot(cfg), "date_utc":datetime.now(timezone.utc).isoformat()}
    g.atomic_json(STUDY / "congelamento.json", {"id":g.digest(value), "value":value})


def verify_freeze():
    require_human_reference()
    path = STUDY / "congelamento.json"
    if not path.exists():
        raise ValueError("Congelamento da avaliação final pendente")
    record = g.read_json(path)
    value = record["value"]
    if record["id"] != g.digest(value) or value["sources"] != source_hashes():
        raise ValueError("Arquivos alterados após o congelamento")
    models = g.Ollama(g.config()).identities()
    if models != value["models"] or g.load_index(g.config(), models)[2] != value["index_id"]:
        raise ValueError("Modelos ou índice alterados")
    return record


def write_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run():
    frozen = verify_freeze()  # Rejeita antes de inferir ou criar um lote sem referência humana.
    cases, protocol = inputs()
    agenda = schedule(cases, protocol["seed"])
    by_id = {c["id"]:c for c in cases}
    folder = STUDY / ("lote_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir()
    g.atomic_json(folder / "agenda.json", agenda)
    g.atomic_json(folder / "congelamento.json", frozen)
    rows, blind = [], []
    for item in agenda:
        verify_freeze()
        case = by_id[item["case_id"]]
        result = g.run_question(case["question"], "comum", case["id"], case["group"], "evaluation",
                                synthetic=True, channel=case["channel"], response_style=item["response_style"])
        rows.append({**item, "run_id":result["id"], "valid":result["valid"], "action":result["action"],
                     "answer":result["answer"], "seconds":result["seconds"], "error":result.get("error", "")})
        cited = (result.get("generated") or {}).get("source_ids", []) if result["action"] == "allow" else []
        blind.append({"review_id":item["observation_id"], "case_id":case["id"], "question":case["question"],
                      "answer":result["answer"], "sources":"\n".join(c["text"] for c in result["retrieved"] if c["id"] in cited),
                      "secondary_review":item["secondary_review"], "safety":"", "treatment":"", "factual":"",
                      "source_support":"", "clarity":"", "example_quality":"", "reviewer":"", "date":"", "reason":""})
        write_csv(folder / "resultados.csv", rows)
        write_csv(folder / "avaliador_sem_condicao.csv", blind)
    g.atomic_json(folder / "resumo_tecnico.json", {"attempts":len(rows), "losses":sum(not r["valid"] for r in rows),
                  "human_review":"pendente", "efficacy":None})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "ratify", "freeze", "run"])
    parser.add_argument("--csv", type=Path, default=STUDY/"referencia_humana.csv")
    args = parser.parse_args()
    if args.command == "plan":
        cases, protocol = inputs()
        g.atomic_json(STUDY / "agenda_planejada.json", schedule(cases, protocol["seed"]))
    elif args.command == "ratify":
        ratify(args.csv)
    elif args.command == "freeze":
        freeze()
    else:
        run()


if __name__ == "__main__":
    main()
