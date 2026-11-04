# Registro de alterações e pendências — revisão acadêmica

03/11/2026. Escopo autorizado: executar correções do parecer, revisar texto e artefato, preparar avaliação e produzir entregáveis verificáveis. Etapa definida pelo autor: Projeto/TCC I.

## Preservação

- Backup anterior à revisão acadêmica: `historico/Antes_revisao_academica_20261103_223148.zip`, 67 arquivos e manifesto SHA-256 interno.
- Parecer original preservado em `poc/docs/PARECER_ACADEMICO_2026-11-03.md`.
- Piloto de outubro: 11 perguntas/22 execuções, código original `1c7e0b3`; transcrições e identificadores mantidos em `poc/docs/pilot_evidence.json`.
- Ficha de tema em Word e cronograma PDF anteriores foram preservados como antecedentes. O título, a etapa e o planejamento vigentes nesta entrega são os do texto revisado e do protocolo; aqueles documentos anteriores não foram apresentados como novos formulários institucionais aprovados.

## Mudanças no texto

Reestruturado em fonte principal e capítulos editáveis `texto/`. Título, problema, objetivo, resumo, abstract e considerações finais tratam desenvolvimento/verificação preliminar e preparação da avaliação. Retiradas promessas de segurança preservada, recusas eliminadas e eficácia comprovada. O público pretendido foi distinguido do perfil fictício; não foram criados participantes.

Incluídas matrizes de objetivos, parecer, cronograma e materiais. Três figuras próprias em TikZ e pseudocódigo refletem o fluxo atual. Conferidos recortes do índice e BNCC oficial. Busca narrativa realizada/logada; Rath atualizado para a publicação formal; NeMo/Llama Guard diferenciados das ferramentas executadas. Referência lexical de Martínez retirada do argumento porque as respectivas métricas não são calculadas neste protocolo; original preservado.

Denominação institucional corrigida; não há nomes de banca ou assinaturas inventados. O manual disponível no portal do curso foi consultado (capa 2025, histórico interno 2024). Margens, recuo e espaçamento ajustados; resumo em um parágrafo e quatro palavras-chave por idioma. Fonte local Times New Roman, com cópias apenas temporárias na cache, e substituta TeX Gyre Termes no pacote portátil. Sem certificação integral ABNT ou decisão de aprovação.

## Mudanças técnicas e evidências

As correções de segurança anteriores constam de `poc/docs/CORRECOES_2026-11-03.md`; não são atribuídas ao piloto original. Nesta revisão:

1. GK-P1.1 acrescentou reconhecimento de ajuda e mensagens fixas em perigo, ofensas, substâncias e desconforto sexual; testes de regra e 54 execuções preservados. Congelamento `7c3f22ac02d49fee515eb08c9d80f335f8dc815ac7980654d819633f57f47573`.
2. O lote revelou omissão/valor falso no novo campo. GK-P1.2 tornou `help_seeking` obrigatório e acrescentou exemplos de intenção. Novo lote de 54 execuções, congelamento `bcc1ae75d57c9be4aec61122767e930478ebbd4a8efb879af4c04840154ac338`. As seis perguntas de ajuda tiveram orientação nas duas condições; controles de dano foram bloqueados. Não houve avaliação humana do conteúdo.
3. Falhas remanescentes preservadas: decomposição classificada como predação; bloqueio na ablação; sustentação reprovada no caso falcão/esquilo. Não houve ajuste com os 40 casos finais.
4. Sondagem de recuperação: 27 perguntas de desenvolvimento; limiares 0,35/0,45/0,55 com 20/6/6 passagens. Mantido 0,45 como referência histórica, sem afirmar ótimo.
5. Instrumentação executável para agenda, ratificação, congelamento e avaliação final condicionada. Analisador final de métricas separado em `poc/metrics.py`, com não executadas distintas de perdas, grupos/categorias, indicadores pareados e agregação descritiva por pergunta. Esse refinamento analítico ocorreu após o lote GK-P1.2 e não altera inferência. O congelamento ativo posterior inclui a instrumentação final; não se atribuem as execuções antigas a esse novo hash.
6. Materiais: 40 perguntas em 20 famílias, duas repetições/duas condições=160 oportunidades; rubrica, proposta de referência humana vazia, instrumento completo e cópia com condições fisicamente omitidas. 32 saídas secundárias selecionadas antes da execução final.

**Verificação:** 45 testes Python e um teste JavaScript aprovados; 108/108 execuções novas tecnicamente válidas em dois lotes sobre as mesmas 27 perguntas. Isso não representa 108 perguntas independentes. PDF compilado e inspecionado visualmente; planilhas recalculadas, inspecionadas e exportadas, com verificações de estrutura e ausência de erros de fórmula. A edição remota no Overleaf e a abertura no Microsoft Excel não foram realizadas; o pacote Overleaf foi compilado localmente em pasta isolada.

## Pendências externas objetivas

| Responsável necessário | Pendência e critério de encerramento |
|---|---|
| Autor e orientador | Aprovar o recorte e o protocolo TCC I; confirmar orçamento de revisão e datas reais. Ajustar ficha institucional do tema se exigida pela disciplina. |
| Revisor humano com domínio do tema | Ler cinco recortes e 40 casos; confirmar/corrigir categoria, apoio e tratamento antes das respostas finais, com data e justificativa. |
| Revisor pedagógico/científico | Conferir adequação curricular, simplificações dos textos e critérios de clareza. Não substituir por afirmação de compreensão infantil. |
| Avaliadores | Fazer 160 julgamentos primários e 32 secundários, se a capacidade for ratificada; preservar discordâncias e consenso/inconclusivos. |
| Autor/orientador, antes de redistribuição pública | Conferir licença, créditos e condições das obras e recortes. Não foram incluídos livros integrais ou pesos dos modelos no pacote da entrega. |
| Disciplina/instituição | Conferir apresentação e fonte no ambiente final, elementos exigidos para esta etapa e nomes/documentos de banca quando oficialmente definidos. |

## Continuidade local que depende dessas etapas

Ratificar o CSV → recongelar → executar a agenda final sem ajustes → regenerar planilhas com respostas → revisão humana parcialmente cega → exportar julgamentos e calcular indicadores → discutir falhas, perdas e inconclusivos. Tudo permanece planejado; nenhum resultado comparativo final foi inventado. Os dados e comandos necessários estão em `PROTOCOLO.md`.

Não foi feito commit, push, publicação, envio de mensagens ou início de serviço pago. O serviço temporário de inferência local foi utilizado apenas para os casos fictícios e encerrado ao terminar os testes.
