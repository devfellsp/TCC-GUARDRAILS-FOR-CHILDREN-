# Relatório de alterações da POC GuardKids

**Data:** 04/11/2026  
**Versão atual:** GK-P2.0-dev  
**Etapa:** desenvolvimento, sem participação de crianças.  
**Estado do serviço:** desligado; não foi iniciado nesta revisão.

## 1. O que foi solicitado

Adotar uma regra de proteção comum aos quatro chats; comparar a explicação direta com a explicação passo a passo; preparar a avaliação de dúvidas educativas, pedidos prejudiciais, pedidos de ajuda e perguntas sem apoio nas fontes; renomear a área da interface para “Regra de proteção”.

## 2. O que mudou na interface

A área “Configuração do experimento” passou a se chamar **Regra de proteção**. Ela explica o comportamento esperado do GuardKids em linguagem simples. O seletor entre “Referência” e “Ajustada” foi removido: a proteção comum é fixa nos quatro chats.

O seletor de linguagem continua separado: **Direto** ou **Passo a passo · com exemplos**. O segundo permanece como opção inicial da interface. O resultado também identifica a proteção comum e o estilo escolhido. A busca e a explicação continuam limitadas ao acervo do chat selecionado.

## 3. Como a regra comum funciona

| Situação identificada | Comportamento esperado |
|---|---|
| Dúvida educativa com apoio nas fontes | Responder e indicar as fontes. Inclui predação educativa não gráfica. |
| Pedido para causar dano, humilhar ou substituir instruções | Recusar conforme a classificação de proteção. |
| Pedido de ajuda ou situação que exige cuidado | Oferecer orientação fixa de cuidado, conforme a categoria. |
| Pergunta sem apoio suficiente no acervo | Informar a falta de base para responder. |
| Falha de modelo, prazo, índice ou processamento | Registrar falha técnica; não contá-la como proteção correta. |

Privacidade e autolesão preservam o encaminhamento fixo já existente. A regra depende das classificações do sistema: esses comportamentos são objetivos da implementação e podem falhar. O estilo da linguagem não afrouxa a proteção e não autoriza acrescentar fatos sem fontes.

## 4. Como será feita a comparação

Foram reutilizados os **16 casos fictícios de desenvolvimento**, quatro em Ciências, quatro em História, quatro em Geografia e quatro no Geral. Cada chat tem um caso educativo, um sem apoio no acervo, um de risco e um de ajuda. As ações esperadas continuam sendo propostas assistidas por IA, pendentes de revisão humana.

Foi preparada uma agenda com **32 tentativas: 16 perguntas × 2 estilos**. Para cada pergunta, mantêm-se a regra comum, o chat, o perfil fictício, as fontes, o modelo e os parâmetros; muda somente a instrução de linguagem. As perguntas são embaralhadas e a ordem inicial dos estilos é equilibrada: oito perguntas começam pelo Direto e oito pelo Passo a passo.

O executor foi atualizado para salvar a agenda antes do lote e os resultados após cada tentativa. Conserva falhas técnicas sem repetir seletivamente as perguntas. Guarda identificação da execução, condição, tempo, resposta e snapshot. Os campos de revisão humana ficam vazios. Recusas e orientações fixas podem ser idênticas nos dois estilos; a comparação de clareza faz mais sentido nas explicações efetivamente geradas.

## 5. Verificações realizadas

| Verificação | Resultado |
|---|---|
| Testes automatizados Python | **69 passaram**. |
| Teste do código da interface | **1 passou**. |
| Configuração ativa | Apenas `comum`, permitindo predação educativa. |
| Seleção das regras antigas pela API | Rejeitada antes de chamar o modelo. |
| Fluxo educativo e bloqueio de dano nos quatro chats e dois estilos | Verificado com respostas simuladas, sem inferência real. |
| Agenda pareada | 32 entradas sobre 16 perguntas; mesma pergunta, chat e regra dentro de cada par. |
| Falha técnica no executor | Preservada, com revisão humana vazia e sem repetição seletiva. |
| Serviço local da POC | Sem serviço escutando na porta 8765 na conferência. |

**As 32 respostas do novo lote não foram executadas.** Os testes acima verificam a implementação e usam simulações onde necessário. Não constituem avaliação de segurança do modelo, qualidade pedagógica ou compreensão por crianças. Nenhum serviço ou modelo foi iniciado nesta revisão.

## 6. O que foi preservado e quais são os limites

Os resultados, snapshots, congelamentos e protocolos anteriores foram preservados. O executor do desenho antigo foi impedido de congelar, ratificar, calibrar ou executar aquele desenho com a configuração atual. Assim se evita tratar a regra comum como se fosse a antiga comparação entre Referência e Ajustada. As funções de análise histórica permanecem disponíveis.

O texto acadêmico e os PDFs existentes ainda descrevem o desenho anterior; **não foram reescritos nem recompilados nesta alteração da POC**. A documentação atual do protótipo e um protocolo separado de desenvolvimento foram atualizados para explicar essa diferença. A versão anterior do guia da POC também foi guardada.

Os pequenos acervos de História, Geografia e Geral são rascunhos assistidos por IA e exigem revisão factual e pedagógica independente. Falhas anteriores de sustentação continuam relevantes: o modelo já acrescentou detalhes ausentes das fontes, e seu verificador os liberou. A nova regra comum não resolve automaticamente esse problema.

Esta comparação examina linguagem sob a mesma proteção; não mede o ganho de segurança causado pelos guardrails em relação a um sistema sem proteção. A amostra é pequena, de desenvolvimento e conhecida pelos autores. Os resultados futuros devem ser apresentados por dimensão, chat e tipo de caso, sem transformar toda resposta liberada em acerto.

## 7. Materiais entregues e continuidade

- `poc/LEIA-ME.md`: instruções atuais da POC e do executor.
- `avaliacao/PROTOCOLO_MULTICHAT_DESENVOLVIMENTO.md`: objetivo, comparação, revisão proposta e tratamento das falhas.
- `avaliacao/multichat_desenvolvimento_2026-11-04/agenda.json`: agenda preparada, ainda não executada.
- `poc/docs/verificacao_regra_comum_2026-11-04.json`: resumo das verificações técnicas.
- `poc/docs/LEIA_ME_ANTERIOR_REGRA_COMUM_2026-11-04.md`: guia anterior preservado.

Próximas etapas de pesquisa: revisar os acervos e as referências esperadas, executar o lote de desenvolvimento quando o pesquisador desejar ligar o modelo, revisar as respostas e depois definir o protocolo e o conjunto reservado da avaliação final. A atualização do manuscrito deverá apresentar a mudança de desenho sem reutilizar os denominadores dos experimentos anteriores.
