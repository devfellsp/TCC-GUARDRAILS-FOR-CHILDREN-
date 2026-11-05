"""Gera tabelas de resultados tecnicos a partir dos registros preservados."""
import json
import statistics
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main():
    summaries = []
    all_records = []
    for folder in sorted((ROOT / 'avaliacao/evidencias').glob('desenvolvimento_*')):
        if not folder.is_dir(): continue
        s = json.loads((folder / 'resumo.json').read_text())
        runs = [json.loads(p.read_text(encoding='utf-8')) for p in (folder / 'runs').glob('*.json')]
        assert len(runs) == s['executions'] == 54
        assert len({r['id'] for r in runs}) == 54
        assert len({r['case_id'] for r in runs}) == 27
        version = runs[0]['configuration']['study_version']
        s['version'] = version; s['folder'] = folder.name
        s['help_routes'] = dict(Counter(r['action'] for r in runs if r['case_id'] in {f'devh{i:02}' for i in range(1,7)}))
        s['risk_controls'] = dict(Counter(r['action'] for r in runs if r['case_id'] in {'devh07','devh08'}))
        s['calls'] = dict(Counter(c['stage'] for r in runs for c in r['calls']))
        summaries.append(s); all_records.extend(runs)
    (ROOT/'avaliacao/evidencias/sintese_tecnica.json').write_text(json.dumps({'natureza':'contagem_tecnica_assistida_IA_sem_julgamento_humano','batches':summaries},ensure_ascii=False,indent=2),encoding='utf-8')
    lines = [r'\begin{tabularx}{\textwidth}{L{2.1cm} L{2.2cm} L{1.8cm} L{2.4cm} Y}',r'\toprule Versão & Perguntas / execuções & Perdas & Mediana (s) & Faixa observada (s) \\ \midrule']
    for s in summaries:
        lines.append(f"{s['version']} & 27 / 54 & {s['technical_losses']} & {format(s['seconds_median'], '.3f').replace('.', ',')} & {format(s['seconds_min'], '.3f').replace('.', ',')} a {format(s['seconds_max'], '.3f').replace('.', ',')}"+r' \\')
    lines += [r'\bottomrule\end{tabularx}']
    (ROOT/'generated/development_summary.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    current = summaries[-1]
    lines = [r'\begin{tabularx}{\textwidth}{L{3.7cm} Y Y}',r'\toprule Rota final & Referência & Ajustada \\ \midrule']
    for route in ['allow','block','safe_guidance','redirect']:
        lines.append(r'\texttt{'+route.replace('_',r'\_')+'} & '+str(current['routes'].get('referencia/'+route,0))+' & '+str(current['routes'].get('ajustada/'+route,0))+r' \\')
    lines += [r'\bottomrule\end{tabularx}']
    (ROOT/'generated/development_routes.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summaries,ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
