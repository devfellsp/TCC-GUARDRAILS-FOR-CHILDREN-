"""Empacota o manuscrito vigente e seus suplementos explicitamente selecionados."""
from pathlib import Path
import zipfile

from archive_multichat_evidence import BATCH, verify

ROOT = Path(__file__).resolve().parents[1]


def build(root=ROOT):
    verify(root)
    names = {"main.tex", "document.tex", "unitins.sty", "unitins.png", "imagens/unitins.png",
             "latexmkrc", "README.md", "ENTREGA_LEIA-ME.md", "LEIA-ME_OVERLEAF.md",
             "poc/LEIA-ME.md", "poc/config.json", "poc/corpus_manifest.json", "poc/multichat_cases.json",
             "poc/requirements.txt", "poc/requirements-lock.txt", "poc/docs/pilot_evidence.json",
             "poc/docs/MATERIAIS_E_REPRODUCAO.md", "poc/docs/environment.json",
             "tools/archive_multichat_evidence.py", "tools/package_overleaf.py", "tools/build_assets.py",
             "tools/update_manuscript.py",
             "avaliacao/BUSCA_NARRATIVA.md", "avaliacao/CALCULO_ASCS_2026-11-04.md",
             "avaliacao/REVISAO_PROTOCOLO_2026-11-04.md", "avaliacao/revisao_acervos_multichat_2026-11-04.json",
             "GuardKids_Drawio_rotulos.drawio", "avaliacao/PLANO_ATUALIZACAO_TCC_GK_P2_6.md",
             "avaliacao/APLICACAO_TCC_GK_P2_6.md", "poc/docs/AMPLIACAO_MATERIAS_2026-11-05.md",
             "poc/tests/test_school_subjects.py", "poc/tests/test_school_subjects_web.cjs",
             "avaliacao/evidencias/ambiente_hardware.json", "avaliacao/evidencias/calibracao_desenvolvimento.json",
             "avaliacao/COMPARACAO_GUARDRAILS_2026-11-05.md",
             "avaliacao/REALINHAMENTO_FICHA_2026-11-05.md",
             "avaliacao/REVISAO_MARCACOES_INTRODUCAO_2026-11-05.md"}
    patterns = ["texto/*.tex", "generated/*.tex", "fontes/*.ttf", "diagramas/pdf/*.pdf", "diagramas/drawio/*.drawio",
                "poc/*.py", "poc/*.ps1", "poc/*.cmd", "poc/web/*.html", "poc/prompts/*.txt",
                "poc/corpus/*.txt", "avaliacao/congelamentos/*.json",
                "poc/versions/GK-P2.6-dev/*.py", "poc/versions/GK-P2.6-dev/*.json",
                "poc/versions/GK-P2.6-dev/*.md", "poc/versions/GK-P2.6-dev/*.cmd",
                "poc/versions/GK-P2.6-dev/prompts/*.txt", "poc/versions/GK-P2.6-dev/web/*.html",
                "poc/versions/GK-P2.6-dev/indice_preservado/*",
                "poc/versions/GK-P2.6-dev/indice_preservado/*/*"]
    for pattern in patterns:
        names.update(p.relative_to(root).as_posix() for p in root.glob(pattern) if p.is_file())
    for folder in [root / BATCH, *sorted((root / "avaliacao/evidencias").glob("desenvolvimento_20261103_*"))]:
        names.update(p.relative_to(root).as_posix() for p in folder.rglob("*") if p.is_file())
    for name in ("README.md", "casos.json", "protocolo.json", "agenda_planejada.json", "referencia_humana.csv",
                 "parecer_primario.csv", "parecer_secundario.csv", "conciliacao.csv", "comparacao_clareza.csv"):
        names.add("avaliacao/final_multichat_v1/" + name)
    # Lista permitida: nunca varrer poc/runs, ambientes, índices locais ou lotes finais.
    target = root / "Overleaf_TCC_Drawio_rotulos.zip"
    temp = target.with_suffix(".zip.tmp")
    try:
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(names):
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                archive.writestr(entry, (root / name).read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
        with zipfile.ZipFile(temp) as archive:
            if archive.testzip() is not None:
                raise ValueError("Pacote corrompido")
            assert all(archive.read(n) == (root / n).read_bytes() for n in archive.namelist())
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)
    return target


if __name__ == "__main__":
    print(build())
