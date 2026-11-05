"""Template histórico preservado para consulta; execução de escrita desativada."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

MAIN = r'''% !TeX program = xelatex
% Overleaf: Settings > Compiler > XeLaTeX; Main document = main.tex.
\PassOptionsToPackage{hyphens}{url}
\documentclass[12pt,openany,oneside,a4paper,english,brazil]{abntex2}
\usepackage{fontspec}
\IfFileExists{.cache/fontes/times.ttf}{
  \setmainfont[Path=.cache/fontes/,BoldFont=timesbd.ttf,ItalicFont=timesi.ttf,BoldItalicFont=timesbi.ttf]{times.ttf}
}{\setmainfont[BoldFont=texgyretermes-bold.otf,ItalicFont=texgyretermes-italic.otf,BoldItalicFont=texgyretermes-bolditalic.otf]{texgyretermes-regular.otf}}
\usepackage{indentfirst,graphicx,microtype,xurl,booktabs,tabularx,array,float,amsmath,amssymb}
\usepackage[portuguese,ruled,linesnumbered]{algorithm2e}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta}
\usepackage{unitins}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\setlrmarginsandblock{3cm}{2cm}{*}
\setulmarginsandblock{3cm}{2cm}{*}
\checkandfixthelayout
\setlength{\parindent}{1.25cm}
\setlength{\parskip}{0pt}
\OnehalfSpacing
\Urlmuskip=0mu plus 2mu\relax
\emergencystretch=3em
\tolerance=1500
\hbadness=10000
\titulo{Desenvolvimento e avaliação de guardrails configuráveis em uma prova de conceito de chatbot educativo destinado a crianças de 7 a 11 anos em português brasileiro}
\autor{Filipe Martins Henrique}
\local{Palmas}
\data{2026}
\orientador{Prof. Marcos Souza}
\instituicao{Universidade Estadual do Tocantins -- UNITINS\par Curso de Sistemas de Informação}
\tipotrabalho{Projeto de Pesquisa -- TCC I}
\preambulo{Projeto de Pesquisa apresentado à disciplina de Trabalho de Conclusão de Curso I do Curso de Sistemas de Informação da Universidade Estadual do Tocantins -- UNITINS, sob orientação do Prof. Marcos Souza.}
\hypersetup{hypertexnames=false,pdftitle={Prova de conceito -- Projeto/TCC I},pdfauthor={Filipe Martins Henrique},colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black,bookmarksdepth=3}
\begin{document}
\frenchspacing
\imprimircapa
\imprimirfolhaderosto*

\begin{resumo}
Chatbots educativos baseados em grandes modelos de linguagem podem produzir respostas inadequadas ou recusar dúvidas escolares legítimas. Este Projeto de Pesquisa/TCC I tem por objetivo desenvolver e verificar funcionalmente uma prova de conceito (PoC) com guardrails contextuais em português brasileiro, e preparar uma avaliação rastreável de segurança e atendimento educativo. O público destinatário pretendido é de sete a onze anos, mas o recorte operacional utiliza apenas um perfil fictício de nove anos, em Ciências do quarto ano, sem participantes infantis. A pesquisa aplicada combina Qwen3:8b, recuperação com BGE-M3 sobre cinco recortes didáticos e verificações de entrada, sustentação e saída. Comparam-se uma ablação conservadora e uma configuração que permite predação educativa. Foram realizados testes automatizados, sondagem de três limiares e dois lotes de desenvolvimento de 54 execuções cada, preservando falhas e versões. Esses procedimentos examinam funcionamento e calibração preliminar; não demonstram segurança geral, compreensão por crianças ou eficácia educativa. Para a continuidade, foram preparados 40 enunciados em 20 famílias, duas condições, duas repetições, rubrica multidimensional e instrumentos de revisão com ocultação parcial das condições. A ratificação das referências e o julgamento humano das respostas permanecem pendentes. A contribuição consiste na operacionalização documentada de políticas contextuais e em um protocolo que distingue rota técnica, segurança, correção factual, fidelidade às fontes e atendimento educativo.

\vspace{\onelineskip}\noindent\textbf{Palavras-chave}: Guardrails. Chatbot educativo. Segurança infantil. Geração aumentada por recuperação.
\end{resumo}
\begin{resumo}[Abstract]
\begin{otherlanguage*}{english}
Educational chatbots based on large language models may produce inappropriate responses or refuse legitimate school questions. This research proposal, submitted as TCC I, aims to develop and functionally verify a proof of concept (PoC) with contextual guardrails in Brazilian Portuguese, and prepare a traceable evaluation of safety and educational responsiveness. The intended audience is children aged seven to eleven; however, the operational scope uses only a fictional nine-year-old profile and fourth-grade science, with no child participants. This applied development study combines Qwen3:8b, BGE-M3 retrieval over five textbook excerpts, and input, grounding and output checks. A conservative ablation is compared with a configuration allowing educational predation. Automated tests, a three-threshold retrieval probe and two development batches of 54 executions each were conducted, preserving failures and version identifiers. These procedures examine technical functioning and preliminary calibration; they do not establish general safety, children's comprehension or educational effectiveness. For subsequent evaluation, 40 questions in 20 families, two conditions, two repetitions, a multidimensional rubric and review instruments with partially concealed conditions were prepared. Human ratification of the reference labels and assessment of response content remain pending. The contribution is a documented implementation of contextual policies and a protocol that distinguishes technical routing, safety, factual correctness, source fidelity and educational responsiveness.

\vspace{\onelineskip}\noindent\textbf{Keywords}: Guardrails. Educational chatbot. Child safety. Retrieval-augmented generation.
\end{otherlanguage*}
\end{resumo}
\pdfbookmark[0]{\listfigurename}{lof}
\listoffigures*
\cleardoublepage
\pdfbookmark[0]{\listtablename}{lot}
\listoftables*
\cleardoublepage
\begin{siglas}
\item[ASCS] Atendimento seguro, correto e sustentado
\item[BNCC] Base Nacional Comum Curricular
\item[IA] Inteligência artificial
\item[JSON] JavaScript Object Notation
\item[LLM] Large Language Model
\item[PoC] Prova de conceito
\item[RAG] Retrieval-Augmented Generation
\item[SHA-256] Secure Hash Algorithm de 256 bits
\item[TCC] Trabalho de Conclusão de Curso
\item[UNITINS] Universidade Estadual do Tocantins
\end{siglas}
\pdfbookmark[0]{\contentsname}{toc}
{\setlength{\cftbeforechapterskip}{0.6em}\tableofcontents*}
\cleardoublepage
\textual
\pagestyle{simple}
\aliaspagestyle{chapter}{simple}
\input{texto/01_introducao.tex}
\input{texto/02_referencial.tex}
\input{texto/03_metodologia.tex}
\input{texto/05_evidencias.tex}
\input{texto/06_consideracoes.tex}
\postextual
\input{texto/referencias.tex}
\end{document}
'''

if __name__ == '__main__':
    raise SystemExit('Gerador histórico desativado: não sobrescrever main.tex. '
                     'Edite as fontes vigentes e use tools/package_overleaf.py para empacotar.')
