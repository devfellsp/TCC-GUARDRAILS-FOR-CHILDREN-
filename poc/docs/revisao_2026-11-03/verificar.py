"""Executa as verificacoes de regressao atuais, sem regravar as evidencias historicas.
As vulnerabilidades da auditoria inicial foram corrigidas; os resultados originais
permanecem em evidencias.json e RELATORIO.md.
"""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[3]
    raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "poc/tests", "-q"], cwd=root))
