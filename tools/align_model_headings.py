"""Aplica a estrutura do modelo UNITINS, preservando os textos do GuardKids."""
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT / name).read_text(encoding='utf-8')

def write(name, value):
    (ROOT / name).write_text(value, encoding='utf-8')

def sections(value):
    parts = re.split(r'\\section\{([^}]+)\}\s*', value)
    return parts[0], dict(zip(parts[1::2], parts[2::2]))

def main():
    backup = ROOT / 'historico/Antes_topicos_modelo_20261104.zip'
    if backup.exists():
        raise RuntimeError('A transformação já foi iniciada; não repetir sobre os arquivos editados.')
    with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in [ROOT/'main.tex', ROOT/'tools/update_manuscript.py', ROOT/'Overleaf_TCC_GuardKids.zip', ROOT/'output/pdf/TCC_GuardKids_TCCI_revisado.pdf', *sorted((ROOT/'texto').glob('*.tex'))]:
            archive.write(p, p.relative_to(ROOT))

    original = 'Desenvolvimento e avaliação de guardrails configuráveis em uma prova de conceito de chatbot educativo destinado a crianças de 7 a 11 anos em português brasileiro'
    for name in ['main.tex', 'tools/update_manuscript.py']:
        value = re.sub(r'\\titulo\{[^}]+\}', lambda _: r'\titulo{' + original + '}', read(name))
        value = value.replace('\\input{texto/04_artefato.tex}\n', '')
        write(name, value)

    intro = read('texto/01_introducao.tex')
    intro = intro.replace(r'\section{Problema e questão de pesquisa}', r'\section{Motivação}')
    intro = intro.replace('\\section{Justificativa e contribuição}\n', '')
    intro = intro.replace('O objetivo geral é', '\\subsection{Objetivo geral}\n\nO objetivo geral é')
    intro = intro.replace('São objetivos específicos:', '\\subsection{Objetivos específicos}\n\nSão objetivos específicos:')
    write('texto/01_introducao.tex', intro)
    write('texto/02_referencial.tex', read('texto/02_referencial.tex').replace('Fundamentação e revisão narrativa', 'Referencial teórico', 1))

    _, method = sections(read('texto/03_metodologia.tex'))
    _, artifact = sections(read('texto/04_artefato.tex'))
    params, figure = method['Parâmetros, calibração e congelamento'].split('\\begin{figure}', 1)
    method_text = '\\chapter{Metodologia}\\label{cap:metodo}\n\n'
    method_text += '\\section{Descrição do Problema}\n\n' + method['Natureza e etapas do estudo']
    method_text += '\\section{Materiais}\n\n\\subsection{Acervo e índice ativo}\n\n' + artifact['Acervo e índice ativo']
    method_text += '\\subsection{Parâmetros, calibração e congelamento}\n\n' + params
    method_text += '\\input{texto/04_artefato.tex}\n\n\\section{Protocolo de avaliação}\n\n'
    for heading in ['Comparação e expectativas verificáveis', 'Casos, exposição e capacidade de revisão', 'Referência de apoio e ordem de execução', 'Rubrica, ocultação e indicadores']:
        method_text += '\\subsection{' + heading + '}\n\n' + method[heading]
    method_text += '\\begin{figure}' + figure
    write('texto/03_metodologia.tex', method_text)
    artifact_text = '\\section{Implementação dos métodos}\\label{cap:artefato}\n\n'
    for heading in ['Versão e fluxo efetivo', 'Políticas contextuais e busca de ajuda', 'Algoritmo e registros']:
        new_heading = 'Pseudocódigos' if heading == 'Algoritmo e registros' else heading
        artifact_text += '\\subsection{' + new_heading + '}\n\n' + artifact[heading]
    write('texto/04_artefato.tex', artifact_text)

    results = read('texto/05_evidencias.tex').replace('Evidências preliminares e discussão', 'Resultados', 1)
    results = results.replace('\\section{Funcionamento técnico e identificação dos lotes}', '\\section{Introdução}')
    results = results.replace('\\begin{table}', '\\section{Apresentação de resultados}\n\n\\subsection{Funcionamento técnico e identificação dos lotes}\n\n\\begin{table}', 1)
    for heading in ['Falha detectada e alteração de desenvolvimento', 'Predação, decomposição e sustentação', 'Piloto histórico preservado', 'Alcance das evidências preliminares']:
        results = results.replace('\\section{' + heading + '}', '\\subsection{' + heading + '}')
    write('texto/05_evidencias.tex', results)

    conclusion = read('texto/06_consideracoes.tex').replace('Considerações finais e continuidade', 'Conclusão', 1)
    head, future = conclusion.split('\\section{Cronograma das etapas de avaliação}', 1)
    schedule, limits = future.split('\\section{Limitações e alternativas}', 1)
    limitation, possibilities = limits.strip().split('\n\n', 1)
    conclusion = head + limitation + '\n\n\\section{Trabalhos futuros}\n\n' + possibilities
    conclusion += '\n\n\\subsection{Cronograma das etapas de avaliação}' + schedule
    conclusion = conclusion.replace('Capítulo~\\ref{cap:artefato}', 'Seção~\\ref{cap:artefato}')
    write('texto/06_consideracoes.tex', conclusion)
    print('Estrutura do modelo aplicada; textos preservados e cópia anterior arquivada.')

if __name__ == '__main__':
    main()
