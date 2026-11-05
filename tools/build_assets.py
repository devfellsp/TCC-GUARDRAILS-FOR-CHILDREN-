"""Gera transcricoes verificaveis e o pacote Overleaf a partir de uma fonte unica."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tex(value):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
                    "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(replacements.get(c, c) for c in value)


def build():
    evidence = json.loads((ROOT / "poc/docs/pilot_evidence.json").read_text(encoding="utf-8-sig"))
    selected = [r for r in evidence["runs"] if r["policy"] == "ajustada" and r["case_id"] in {"dev01", "dev02", "dev03"}]
    if len(selected) != 3 or len({r["case_id"] for r in selected}) != 3:
        raise ValueError("Evidencias ausentes ou duplicadas")
    lines = ["% Gerado por tools/build_assets.py; transcricao exata de pilot_evidence.json.",
             r"\begin{tabularx}{\textwidth}{L{1.0cm} Y L{2.45cm} L{2.0cm} L{3.0cm}}",
             r"\toprule",
             r"\textbf{Caso} & \textbf{Resposta literal (política ajustada)} & \textbf{Fontes citadas} & \textbf{Rubrica (Corr. / Pert. / Clar.)} & \textbf{Rastreabilidade e situação do julgamento} \\",
             r"\midrule"]
    for index, run in enumerate(sorted(selected, key=lambda r: r["case_id"])):
        sources = ", ".join(r"\nolinkurl{" + s + "}" for s in run["source_ids"])
        # Identificador completo em duas linhas evita transbordo de uma palavra hexadecimal longa.
        run_id = run["run_id"]
        identifier = r"\texttt{" + run_id[:16] + r"}\newline\texttt{" + run_id[16:] + "}"
        note = "Registro: " + identifier + r"\newline Política ajustada. Julgamento humano ainda não registrado."
        lines.append(r"\texttt{" + tex(run["case_id"]) + "} & " + tex(run["answer"]) + " & " + sources
                     + " & Pendente / Pendente / Pendente & " + note + r" \\")
        if index < len(selected) - 1:
            lines.append(r"\addlinespace[3pt]")
    lines.extend([r"\bottomrule", r"\end{tabularx}"])
    generated = ROOT / "generated"
    generated.mkdir(exist_ok=True)
    (generated / "pilot_responses.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "document.tex").write_text("% !TeX program = xelatex\n% Entrada de compatibilidade: a fonte principal e main.tex.\n\\input{main.tex}\n", encoding="utf-8")
    main = "\n".join(p.read_text(encoding="utf-8-sig") for p in [ROOT / "main.tex", *sorted((ROOT / "texto").glob("*.tex"))])
    labels = re.findall(r"\\label\{([^}]+)\}", main)
    refs = re.findall(r"\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}", main)
    if len(labels) != len(set(labels)) or set(refs) - set(labels):
        raise ValueError("Rotulos duplicados ou referencias internas ausentes")
    from package_overleaf import build as package_overleaf
    package_overleaf(ROOT)
    print("Transcricoes e pacote vigente Overleaf_TCC_Drawio_rotulos.zip atualizados.")


if __name__ == "__main__":
    build()
