# Atendimento às marcações da introdução

Data: 05/11/2026. Documento de referência: C:/Users/Filipe/Downloads/Revisoes Marcado.pdf.

O autor definiu vermelho como trecho a retirar ou reformular e amarelo como ponto de atenção. A revisão anterior realinhou o foco à ficha do tema, mas deixou parte das marcações pendente. Esta revisão completa o tratamento da introdução, preservando o diagrama 1 novo e a decisão aprovada sobre proteção como foco principal e estilos como análise complementar.

## Vermelho

| Local no PDF anotado | Tratamento no manuscrito |
| --- | --- |
| Página 1: frase sobre a adequação do protótipo depender de evidências | Retirada. O parágrafo termina nas referências sobre riscos e necessidades infantis. |
| Página 1: histórico da ampliação de Ciências e enumeração de ausências de participantes e medidas | Retirados da introdução. A apresentação passa a descrever o perfil fictício e o acervo atual. Os limites metodológicos e o histórico continuam nos capítulos pertinentes. |
| Página 1: verificação preliminar concentrada no comportamento técnico | Substituída pela explicação concreta do que os testes verificaram e do que será julgado na avaliação humana. |
| Página 2: pedido para ferir um animal | Aplicada a formulação do comentário: “pedido sobre como ferir um animal”. O parágrafo também acompanha os resultados e as dimensões do diagrama novo. |
| Página 2: pergunta de pesquisa centrada em dois estilos | Substituída pela pergunta alinhada à ficha, sobre configuração de guardrails, respostas inadequadas e bloqueio indevido. A comparação de estilos é complementar. |
| Página 2: execução local, inferência paga, corpus pequeno e busca narrativa | Parágrafo retirado da introdução. Os detalhes de ambiente, acervo e revisão da literatura permanecem nos capítulos correspondentes. |

## Amarelo

| Local no PDF anotado | Tratamento no manuscrito |
| --- | --- |
| Página 1: apresentação da PoC e comentário sobre privacidade e prompt injection | Apresentação reescrita. Inclui detecção de alguns identificadores, bloqueio de tentativas reconhecidas de substituir instruções e omissão de texto livre nos registros comuns. |
| Página 1: pequeno destaque isolado na apresentação | Abrangido pela reescrita do mesmo parágrafo. |
| Página 1: julgamento humano como etapa posterior | Esclarecida a diferença entre os testes de processamento, consulta, regras e registro já realizados e o julgamento humano previsto. |
| Página 2: resposta correta sem sustentação e avaliação conjunta | Reescrito com distinção direta entre decisão de responder, correção e apoio nas fontes. |
| Página 2: dois estilos, quatro/dez chats e versões, com comentário “Confuso” | Removidos os códigos de versão e a cronologia desse trecho. Dois contrastes explicados separadamente: proteções como principal e estilos como complementar. |
| Página 2: objetivo geral | Reformulado segundo a ficha, com foco em respostas inadequadas e bloqueio indevido, sem confundir o objetivo do projeto com os testes concluídos no TCC I. |
| Página 4: objetivos específicos | Reorganizados em cinco itens legíveis: riscos, implementação, casos e critérios, comparação entre proteções e análise dos efeitos e limites. |

Os destaques verdes sobre a possibilidade de uma recusa impedir uma dúvida legítima e a chamada da figura têm seus sentidos preservados. A indicação do público de sete a onze anos, destacada em rosa, foi mantida.

## Conferência dos quatro comentários

1. Privacidade e prompt injection: incorporados conforme a implementação, com limitação explícita da detecção.
2. Redação sobre como ferir um animal: aplicada.
3. “Não me lembro de ter definido isto”: pergunta realinhada à ficha, conforme aprovação do autor.
4. “Confuso”: texto de estilos e histórico simplificado e separado do contraste principal.

## Precisão das afirmações sobre privacidade

Foram conferidos `poc/versions/GK-P2.6-dev/privacy.py`, `guardkids.py` e `prompts/classifier.txt`. O modo comum omite perguntas, respostas geradas, rascunhos e justificativas dos registros; os testes explicitamente fictícios podem conservar o conteúdo integral. A detecção local cobre alguns padrões e o classificador pode errar. Portanto, a introdução não afirma que nenhum dado pessoal jamais é mantido nem que todo prompt injection é bloqueado. Isso reflete o código e não uma garantia genérica de guardrails.

## Preservação e verificação

O PDF anotado permanece intacto. Backup anterior: historico/Antes_revisao_marcacoes_introducao_20261105.zip. A implementação e os registros experimentais não foram alterados; nenhuma inferência ou avaliação humana foi realizada.

O PDF entregue mantém 45 páginas, oito figuras e dez tabelas. A introdução ocupa as páginas impressas 9 a 11. A compilação e a renderização conferem referências, glifos, paginação e legibilidade. O pacote para Overleaf inclui esta matriz e as fontes atualizadas, conferidas contra os arquivos locais.

## Correção de compatibilidade em 06/11/2026

O autor identificou opções de formatação da lista impressas como texto e uma chamada “Tabela ??” ao abrir o capítulo isolado. A lista passou a usar `enumerate` sem opções de pacote e rótulos explícitos em cada `item`. A chamada de tabela foi substituída por uma frase sobre o desenvolvimento realizado e a avaliação planejada; a menção numerada ao capítulo de metodologia também foi substituída por uma referência textual. A única referência numerada restante é à figura definida na própria introdução.

Foram compilados e inspecionados o documento completo e uma versão isolada com configuração mínima, sem enumitem. Ambos exibem os cinco itens de a) a e), sem opções impressas nem referências “??”. O documento completo mantém 45 páginas e não apresenta caixas Overfull, glifos ausentes ou referências indefinidas. Não houve alteração dos objetivos ou do desenho da pesquisa.
