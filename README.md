# TCC GuardKids

Autor: Filipe Martins Henrique — UNITINS
Orientador: Prof. Marcos Souza

**Projeto/TCC I**, conforme confirmação do autor. GuardKids: desenvolvimento e verificação preliminar de guardrails contextuais em quatro chats educativos. Destinação pretendida de 7–11 anos; perfil operacional fictício de nove anos; sem participantes infantis.

## POC atual — regra comum e comparação de linguagem (04/11/2026)

A versão `GK-P2.1-dev` usa uma regra comum em Ciências, História, Geografia e Geral, com estilos Direto e Passo a passo. A revisão documental precedeu um lote de **32 tentativas executadas sobre 16 perguntas**, sem perdas técnicas. A inspeção preliminar apontou ressalvas de sustentação em cinco das oito explicações liberadas; os campos humanos continuam vazios. As rotas não são indicadores de eficácia.

O conjunto reservado atual tem 32 perguntas em 16 famílias e 64 oportunidades, ainda não executadas. A revisão prospectiva corrigiu o balanceamento da segunda revisão por chat e grupo e formalizou o ASCS no protocolo; seu cálculo final depende de revisão humana. A referência humana e o congelamento permanecem pendentes. O manuscrito e seus diagramas foram atualizados, mantendo as 108 execuções anteriores em seção histórica, sem somar denominadores.

- [TCC revisado em PDF](TCC_GuardKids_Drawio_rotulos.pdf) — 41 páginas, sete figuras Draw.io e um cronograma de Gantt.
- [Projeto revisado para o Overleaf](Overleaf_TCC_Drawio_rotulos.zip) — selecione main.tex e XeLaTeX.
- [Sete diagramas editáveis em um arquivo](GuardKids_Drawio_rotulos.drawio). As fontes individuais estão em diagramas/drawio/ e as figuras do manuscrito em diagramas/pdf/.
- Revisão editorial e bibliográfica aplicada: [registro das correções e verificações](avaliacao/APLICACAO_AUDITORIA.md).
- Relatório: `poc/docs/RELATORIO_PESQUISA_2026-11-04.md`.
- Lote e revisão: `avaliacao/evidencias/multichat_20261104_revisado/`.
- Protocolo final atual: `avaliacao/final_multichat_v1/README.md`.
- Instruções da POC: `poc/LEIA-ME.md`.


## Entrega acadêmica anterior, revisada em 03/11/2026

- Fonte principal: `main.tex`, com capítulos e figuras em `texto/`; compilador XeLaTeX. Instruções em `LEIA-ME_OVERLEAF.md`.
- O PDF e os pacotes dessa entrega anterior foram arquivados fora da pasta ativa.
- Protocolo, rubrica, casos e matrizes: `avaliacao/`; comece por `avaliacao/ALTERACOES_E_PENDENCIAS.md`.
- Planilha completa e cópia com condições omitidas: `outputs/guardkids_revisao_20261103/`.
- Evidências: dois lotes de desenvolvimento (108 execuções sobre 27 perguntas reutilizadas), sondagem e congelamentos em `avaliacao/evidencias/` e `avaliacao/congelamentos/`.

A avaliação final e os julgamentos humanos estão pendentes. Os 40 enunciados reservados e as 160 oportunidades planejadas não foram executados nesta revisão. Há falhas remanescentes de classificação/sustentação discutidas no texto; não se declara eficácia ou segurança geral.

A ficha de tema Word e o cronograma PDF anteriores listados abaixo são antecedentes preservados. O título, a etapa e o cronograma vigentes são os do texto revisado; aprovação institucional não foi presumida.

## Arquivos atuais

- `main.tex`: fonte principal do TCC. `document.tex` é uma entrada de compatibilidade que carrega `main.tex`, sem duplicar o texto. No Overleaf, selecione `main.tex`.
- `ficha_tema_tcc_Filipe_Martins_Henrique_revisada.docx`: ficha de definição do tema.
- `Cronograma.pdf`: cronograma do projeto.
- `Livros_Didadicos/`: as duas apostilas educativas selecionadas, Trilhas (2021) e Livro do Estudante (2024).
- `artigos_e_guias/`: artigos científicos e guia de referência para as políticas de proteção.
- `benchmarks_e_datasets/`: MinorBench e planilhas do conjunto de dados de Martínez.
- `poc/`: implementação local do GuardKids, ambiente Python, configurações, seleção dos trechos, registros e documentação. Comece por `poc/LEIA-ME.md`.

## Executar o protótipo

Com o Ollama aberto, execute `poc/Iniciar_GuardKids.cmd` e abra http://127.0.0.1:8765. As perguntas iniciam sessões independentes. O protótipo está em desenvolvimento; os testes iniciais não são a avaliação final do TCC.

Os diagramas editáveis estão em `diagramas/`; as decisões, em `poc/docs/ARQUITETURA_E_DECISOES.md`. O TCC distingue a rodada histórica da implementação revisada. A avaliação independente e os julgamentos humanos ainda estão pendentes.

## Revisão de 03/11/2026

As correções estão descritas em `poc/docs/CORRECOES_2026-11-03.md`. Os registros comuns omitem texto livre; o executor de desenvolvimento habilita registros completos somente para seus casos fictícios. O índice local anterior pode ser validado e migrado com `poc/.venv/Scripts/python.exe poc/guardkids.py migrate-index`, sem nova inferência.

`poc/docs/pilot_evidence.json` contém as 22 execuções fictícias conferidas do piloto histórico, com identificadores e julgamentos pendentes. `tools/build_assets.py` gera as transcrições e o pacote Overleaf a partir dessa evidência e da fonte principal. Para atualizar uma figura vigente, edite o arquivo Draw.io correspondente e exporte o PDF pelo Draw.io Desktop. A suíte é executada com `python -m pytest poc/tests -q`, usando o ambiente do projeto.

## Histórico

- `historico/Historico_antes_da_organizacao_2026-10-25.zip`: cópia dos materiais locais anteriores à atualização, incluindo modelos, revisões e arquivos auxiliares. Guarde para recuperar algum conteúdo antigo, caso necessário.
- `historico/metodologia_guardkids_revisada.zip`: pacote recebido do Git, preservado como histórico; não foi regenerado a partir do texto atual.
- `historico/Capitulo_3_Metodologia_Versao_Anterior.pdf`: PDF da metodologia anterior.

A atualização copiou os arquivos da pasta recebida do Git e verificou a igualdade de conteúdo antes da limpeza. Em 03/11/2026, esta pasta foi conectada ao [repositório do projeto](https://github.com/devfellsp/TCC-GUARDRAILS-FOR-CHILDREN-), preservando o histórico existente e incluindo o código do protótipo em `poc/`. Ambientes locais, caches, índices gerados e registros individuais de execução ficam fora do versionamento; as decisões e os resumos do piloto estão em `poc/docs/`.

O calculador prospectivo `poc/final_metrics.py` implementa os dois denominadores do ASCS e a conciliação dos pareceres. Sem lote final e revisão humana, informa pendências e mantém as taxas finais vazias. Uso em `avaliacao/final_multichat_v1/README.md`.

As instruções de compilação, execução e conferência dos materiais estão em `poc/docs/MATERIAIS_E_REPRODUCAO.md`, fora do manuscrito.

Os 32 registros completos e o snapshot do lote multidisciplinar estão arquivados em `avaliacao/evidencias/multichat_20261104_revisado/`, com manifesto SHA-256 e ambiente registrado. O pacote Overleaf inclui essas evidências e os lotes históricos selecionados. Para atualizar o pacote, use `python tools/package_overleaf.py`.
