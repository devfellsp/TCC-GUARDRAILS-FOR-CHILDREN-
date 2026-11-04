"""Prepara dados de coleta, sem criar julgamentos ou arquivos XLSX."""
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "poc"))
import evaluation as e

def main():
    cases = json.loads((ROOT / "avaliacao/casos_avaliacao.json").read_text(encoding="utf-8"))
    corpus = json.loads((ROOT / "avaliacao/corpus_referencia.json").read_text(encoding="utf-8"))
    lookup = {c["id"]: c for c in corpus["chunks"]}
    agenda = e.schedule(cases)
    byid = {c["case_id"]: c for c in cases}
    selected = set()
    for group, n in {"G1": 4, "G2": 4, "G3": 4, "G4": 12, "G5": 8}.items():
        for policy in ["referencia", "ajustada"]:
            for repetition in [1, 2]:
                part = [a for a in agenda if byid[a["case_id"]]["group"] == group and a["policy"] == policy and a["repetition"] == repetition]
                part.sort(key=lambda a: hashlib.sha256((a["observation_id"] + "segunda-revisao").encode()).hexdigest())
                selected.update(a["observation_id"] for a in part[:n//4])
    assert len(selected) == 32
    observations = []
    final = {}
    final_pointer = ROOT / "avaliacao/evidencias/avaliacao_final_ativa.json"
    if final_pointer.exists():
        folder = ROOT / json.loads(final_pointer.read_text())["folder"]
        for p in (folder / "runs").glob("*.json"):
            r = json.loads(p.read_text(encoding="utf-8")); final[r["observation_id"]] = r
    for a in agenda:
        c = byid[a["case_id"]]; r = final.get(a["observation_id"], {})
        observations.append({**a, **{k: c[k] for k in ["group", "category", "origin", "question", "expected_treatment", "corpus_support"]},
                             "references": "\n\n".join(k + ": " + lookup[k]["text"] for k in c["reference_ids"]),
                             "answer": r.get("answer"), "action": r.get("action"), "valid": str(r["valid"]).lower() if "valid" in r else "pendente",
                             "seconds": r.get("seconds"), "error": r.get("error"), "output_block": "sim" if r.get("final_origin") == "output_guard" else "nao" if r else None,
                             "second_review_planned": "sim" if a["observation_id"] in selected else "nao", "version": "GK-P1.2"})
    development = []
    for folder in sorted((ROOT / "avaliacao/evidencias").glob("desenvolvimento_*")):
        if folder.is_dir():
            for path in (folder / "runs").glob("*.json"):
                r = json.loads(path.read_text(encoding="utf-8")); development.append(r)
    out = ROOT / ".cache/academico/workbook_payload.json"
    out.write_text(json.dumps({"observations": observations, "cases": cases, "development": development, "corpus": corpus}, ensure_ascii=False), encoding="utf-8")
    fields = ["observation_id", "case_id", "family_id", "group", "category", "origin", "policy", "repetition", "version", "question", "expected_treatment", "corpus_support", "references", "answer", "action", "error", "valid", "seconds", "output_block", "natureza", "avaliador", "data", "justificativa", "seguranca", "factual", "fidelidade", "clareza", "atendimento", "tratamento", "bloqueio_indevido", "redirecionamento_indevido", "insuficiencia_correta", "discordancias", "second_review_planned", "avaliador2", "natureza2", "data2", "justificativa2", "seguranca2", "factual2", "fidelidade2", "clareza2", "atendimento2", "consenso"]
    (ROOT / "avaliacao/dicionario_campos.json").write_text(json.dumps({"columns": fields, "note": "Campos primários em português alimentam metrics; segunda revisão e consenso preservados sem sobrescrever originais. Cabeçalhos ingleses são chaves do protocolo."}, ensure_ascii=False, indent=2), encoding="utf-8")
    key = [{k: a[k] for k in ["observation_id", "case_id", "policy", "repetition", "order", "second_review_planned"]} for a in observations]
    import csv
    with (ROOT / "avaliacao/chave_decodificacao.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=list(key[0])); w.writeheader(); w.writerows(key)
    print(f"{len(observations)} linhas planejadas; {len(development)} registros de desenvolvimento; nenhum julgamento inventado")

if __name__ == "__main__": main()
