# Plano de atualização do TCC para a GK-P2.6-dev

Data: 05/11/2026. Estado: executado e validado.
Projeto: C:/Users/07116358110/Documents/TCC-GUARDRAILS-FOR-CHILDREN--main.

## Decisão editorial

Apresentar a GK-P2.6-dev como artefato atual em desenvolvimento. Manter os experimentos anteriores identificados por versão. Preservar o caráter de TCC I, o perfil fictício de nove anos/quarto ano e a ausência de participantes infantis ou medição de aprendizagem.

Base atual conferida: dez chats, seis PDFs de quatro coleções, três sínteses e 40 blocos. Distribuição: Ciências 7, História 6, Geografia 9, Geral 2, Português 2, Matemática 3, Inglês 3, Arte 3, Educação Física 2 e Tecnologia 3.
Histórico: GK-P2.1 tem quatro chats/oito blocos; a ampliação intermediária chegou a 18 blocos. A GK-P2.6 acrescentou 21 recortes, desdobrados em 22 blocos.

## Fontes de verdade e leitura mínima

- poc/versions/GK-P2.6-dev/VERIFICACAO_ENTREGA.json: contagens, índice, testes e tempos.
- corpus_manifest.json e SELECAO_DO_ACERVO.json na mesma pasta: livros, matérias, páginas, âncoras, hashes e limites.
- config.json, channels.py, LEIA-ME.md e VERIFICACAO_LOCAL.json na mesma pasta.
- poc/docs/AMPLIACAO_MATERIAS_2026-11-05.md: implementação e alcance das verificações.
- main.tex e texto/*.tex: manuscrito.
- diagramas/drawio/ e GuardKids_Drawio_rotulos.drawio: fontes dos sete diagramas (o cronograma LaTeX completa oito figuras).

## Execução em três etapas

### 1. Texto, referências e consistência

[x] Fazer um backup da entrega vigente em historico/ e registrar o estado inicial do Git.
[x] Conferir os dados acima contra os arquivos indicados uma única vez.
[x] Atualizar main.tex (Resumo/Abstract) e texto/01_introducao.tex: escopo atual e objetivos; generalizar números fixos da pergunta de pesquisa quando necessário, preservando o contraste entre estilos.
[x] Revisar texto/02_referencial.tex somente nos vínculos entre teoria e novas matérias/acervos. Manter a fundamentação revisada; acrescentar literatura apenas se houver nova afirmação que exija apoio.
[x] Atualizar texto/03_metodologia.tex: tabela por matéria, seis volumes/quatro coleções, 40 blocos, seleção/exclusões, rastreabilidade, limites curriculares, revisão humana e condições de reutilização.
[x] Atualizar texto/04_artefato.tex: versão, dez chats, filtro por matéria, inicialização, restauração do índice, prazo de 600 s/610 s e gestão de memória.
[x] Organizar texto/05_evidencias.tex por versão. Preservar 32 tentativas, 108 execuções históricas e piloto com seus próprios denominadores. Relatar 25 testes Python, um teste de interface e três consultas reais como verificações de desenvolvimento, sem taxas de eficácia ou generalização aos dez chats.
[x] Identificar o plano reservado de 32 perguntas/64 oportunidades como proposta da GK-P2.1. Registrar que o plano final da GK-P2.6 precisa ser revisto antes de congelar casos e referências, inclusive por mudança do acervo. Não inventar novos quantitativos nem reaproveitar a reserva como se permanecesse independente.
[x] Atualizar texto/06_consideracoes.tex, cronograma e demais trechos incluídos pelo main.tex que ainda descrevam a versão anterior como atual.
[x] Conferir quatro novas entradas bibliográficas, chamadas autor-data e créditos. Distinguir data inferida de data editorial e páginas impressas de páginas físicas do PDF.

### 2. Diagramas do Draw.io

[x] Conferir as sete figuras e alterar apenas o conteúdo afetado por versão, matérias, acervo e avaliação.
[x] Priorizar arquitetura (03), desenho da pesquisa (04) e preparação/consulta (06); conferir também problema (01), análise contextual (02), processamento (05) e proteção (07).
[x] Editar os originais individuais do Draw.io e sincronizar as abas dos arquivos conjuntos.
[x] Exportar pelo Draw.io para os caminhos existentes em diagramas/pdf/. Preservar estilo, legendas, fontes e legibilidade na página.
[x] Manter sete diagramas Draw.io, com originais e PDFs correspondentes, e preservar o cronograma como oitava figura. Não recriar os desenhos com outro gerador.

### 3. Entrega e validação

[x] Atualizar README.md, ENTREGA_LEIA-ME.md e LEIA-ME_OVERLEAF.md.
[x] Gerar Overleaf_TCC_Drawio_rotulos.zip e compilar com XeLaTeX a partir de extração limpa até resolver referências.
[x] Inspecionar páginas alteradas, tabelas, figuras, sumário, referências e logo em todas as páginas.
[x] Entregar TCC_GuardKids_Drawio_rotulos.pdf e o ZIP na raiz; informar paginação final e páginas das alterações relevantes.
[x] Registrar alterações e verificações em uma nota de aplicação. Não fixar previamente o total de páginas.
[x] Respeitada a condição de commit/push somente se solicitado para esta atualização: não solicitado, não executado.

## Regra para economizar tokens

Retomar por este arquivo e pelas fontes de verdade, sem reler todo o chat ou refazer a auditoria anterior. Ler somente trechos afetados; agrupar buscas independentes; aplicar substituições contextualizadas, sem troca global de “quatro” por “dez”. Atualizar os checkboxes e registrar apenas decisões novas e bloqueios concretos.

A atualização documental utiliza os testes já registrados. Reexecutar inferências ou ampliar testes somente se surgir uma mudança funcional ou inconsistência que exija isso. Usar uma rodada principal de revisão e uma compilação final limpa, corrigindo apenas os problemas encontrados.

## Resultado da execução

Entrega com 44 páginas, oito figuras (sete diagramas Draw.io e cronograma), dez tabelas e 24 referências. Compilação XeLaTeX em três passagens a partir de extração limpa do ZIP; referências e listas resolvidas. Detalhes e páginas em APLICACAO_TCC_GK_P2_6.md.
