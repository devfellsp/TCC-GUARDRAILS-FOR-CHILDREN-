# Validação comparativa do GuardKids com o TCC de referência

**Data:** 03/11/2026. **Objeto:** comparar estrutura, apresentação e desenvolvimento acadêmico do GuardKids com o trabalho fornecido pelo autor. Este relatório é material de acompanhamento e não integra o texto do TCC.

**Resultado:** o GuardKids apresenta uma estrutura acadêmica compatível em seus elementos principais, mas não tem o mesmo desenvolvimento teórico e demonstrativo do exemplo. A prioridade é aprofundar a fundamentação e a análise dos testes já realizados, além de corrigir diferenças formais pontuais. A quantidade de páginas, isoladamente, não determina a qualidade nem a aprovação.

## 1. Materiais e procedimento

### Trabalho de referência

- Arquivo recebido: `C:/Users/Filipe/Downloads/Model_TCC_Latex_preenchido(1).zip`.
- Autor: Hugo Cavalcante Lima.
- Título: *Modelagem mono e multiobjetivo para o problema de sequenciamento de tarefas em máquinas paralelas não relacionadas*.
- Ano: 2018; Curso de Sistemas de Informação da UNITINS.
- O ZIP contém o PDF de 56 páginas, fontes LaTeX, bibliografias, figuras, ficha catalográfica e ata de defesa. A leitura visual da ata de 26/06/2018 identifica aprovação e pontuação manuscrita 9,0. A informação é a do documento fornecido, sem consulta a registro acadêmico externo.
- A referência apresenta pesquisa concluída, resultados de algoritmos e conclusão sobre os objetivos. O GuardKids está identificado, por decisão do autor, como Projeto/TCC I, com avaliação humana ainda planejada.

### GuardKids

- PDF comparado: `output/pdf/TCC_GuardKids_TCCI_revisado.pdf`, versão após retirada das notas editoriais.
- Fontes examinadas: `main.tex`, `unitins.sty`, os seis capítulos em `texto/`, figuras, referências e apêndice.
- Materiais complementares considerados: corpus, protocolo, rubrica, evidências de desenvolvimento e registro de hardware.

Foram inspecionados os PDFs e seus sumários, a apresentação das capas, dos objetivos, das figuras, das tabelas e das referências. Também foram lidas a introdução e a conclusão do exemplo e examinadas as seções de fundamentação, materiais, formulação e resultados relevantes à comparação. Os arquivos do ZIP foram tratados como documentos de referência; seus comentários e instruções não foram executados ou adotados como ordens. Não foi feita auditoria matemática integral dos algoritmos de otimização do trabalho de 2018.

O manual institucional obtido no portal do curso em 03/11/2026 foi usado como conferência complementar. A aprovação do trabalho antigo não transforma todas as suas opções de edição em regras atuais.

## 2. O que a paginação realmente mostra

Contagens abaixo usam páginas físicas dos PDFs. Os intervalos compreendem a página de abertura de cada capítulo até a página anterior ao capítulo seguinte; não equivalem a número de páginas inteiramente preenchidas.

| Parte | TCC de referência | GuardKids |
|---|---:|---:|
| Elementos anteriores à introdução | 14 | 8 |
| Introdução | 2 | 2 |
| Fundamentação / referencial | 12 | 3 |
| Metodologia | 15 | 4 |
| Capítulo específico do artefato | Integrado à metodologia | 5 |
| Resultados / evidências preliminares | 9 | 3 |
| Conclusão / considerações finais | 2 | 2 |
| Referências | 2 | 2 |
| Apêndice de reprodução | 0 | 2 |
| **Total físico** | **56** | **31** |
| **Da introdução ao fim da conclusão** | **40** | **19** |

O exemplo tem seis páginas a mais de elementos anteriores à introdução: aprovação, ficha catalográfica, dedicatória, agradecimentos, epígrafe e uma página adicional de sumário. A diferença do corpo é maior: **21 páginas**. O apêndice do GuardKids acrescenta duas páginas, de modo que a diferença total é de 25.

Portanto, a redução não decorreu apenas de fonte, margens ou retirada de elementos opcionais. O referencial foi muito mais condensado. Na metodologia, deve-se considerar conjuntamente o protocolo e o capítulo do artefato do GuardKids: são nove páginas, comparadas às quinze do exemplo. A extensão dos resultados também reflete a diferença entre um estudo concluído e uma avaliação ainda preliminar.

**Não há, nessa comparação, exigência de transformar o GuardKids em um documento de 56 páginas.** O manual consultado, seção 7.1.15, descreve para monografia o intervalo de 30 a 60 páginas, incluindo partes pré-textual, textual e pós-textual. Assim, não seria correto afirmar que o GuardKids está abaixo desse intervalo por ter 19 páginas de corpo. A aplicação das exigências de monografia a um Projeto/TCC I precisa seguir as orientações da disciplina. A necessidade de aprofundamento apontada aqui decorre do conteúdo, não de uma meta artificial de páginas.

## 3. Matriz de comparação

| Critério | Evidência no exemplo | Situação do GuardKids | Avaliação |
|---|---|---|---|
| Base LaTeX | Classe `abntex2`, customização `unitins`, A4, tamanho-base 12 | Mesma classe e customização, A4 e tamanho-base 12 | Compatível na base estrutural. |
| Logotipo e capa | Logotipo UNITINS, curso, título, autor, local e ano | Mesmos elementos; o arquivo de logotipo tem SHA-256 idêntico | Compatível. Diferenças de quebra do título decorrem de seu comprimento. |
| Folha de rosto | O PDF fornecido apresenta título, autor e preâmbulo sem logotipo nessa página | A folha atual do GuardKids inclui logotipo e identificação do curso | Diferença visual; não é prova isolada de erro. O próprio `unitins.sty` do ZIP inclui logotipo na folha de rosto, diferindo do PDF fornecido. |
| Fonte principal | PDF e fonte indicam Latin Modern | PDF local usa Times New Roman; versão portátil tem TeX Gyre Termes como alternativa | Não é reprodução tipográfica exata. O manual consultado indica Times New Roman ou Arial; por isso não se deve trocar automaticamente para Latin Modern apenas para imitar o exemplo. |
| Parágrafos | Fonte configura recuo de 1,3 cm e espaço de 0,2 cm entre parágrafos | Recuo de 1,25 cm e espaço adicional zero | Diferença de edição. O recuo de 1,25 cm corresponde ao manual consultado; a diferença de espaço entre parágrafos deve ser tratada como escolha de apresentação, não como falha científica. |
| Estrutura principal | Introdução, referencial, metodologia, resultados e conclusão | Possui os mesmos componentes, com separação adicional do artefato | Compatível em conteúdo estrutural. Não é obrigatório reduzir a seis ou cinco capítulos por imitação. |
| Objetivos | Objetivo geral e objetivos específicos aparecem em subseções; os específicos são listados | Geral e específicos estão em dois parágrafos de uma seção única | Melhorar a identificação e a leitura, separando as subseções sem alterar o alcance dos objetivos. |
| Fundamentação | Conceitos são definidos, subdivididos e relacionados aos métodos; há exemplos, equações, figuras e citações | Três páginas concentram busca narrativa, trabalhos, RAG e recorte curricular | Principal necessidade de aprofundamento. O texto apresenta as referências, mas explica brevemente os mecanismos que sustentam as decisões do sistema. |
| Trabalhos relacionados | Estudos sustentam conceitos e métodos ao longo do referencial | Há quadro de referências, contribuição aproveitada e limites | Elemento existente e pertinente. Pode ganhar critérios uniformes: público, idioma, riscos, método de proteção e tipo de avaliação. |
| Metodologia e materiais | Descreve problema, dados de entrada, ambiente, ferramentas e procedimentos | Protocolo e fluxo estão documentados; hardware está em arquivo complementar | Levar para o capítulo os dados de ambiente relevantes à interpretação da latência, sem transformar o capítulo em manual de instalação. |
| Resultados demonstrados | Apresenta saídas dos algoritmos, tabelas por problema, estatísticas e gráficos | Apresenta contagens de rotas, tempos e discussão de casos, com respostas completas nos arquivos externos | Melhorar a demonstração: incluir algumas perguntas, respostas literais e trechos de apoio dos registros de desenvolvimento. Manter julgamento humano identificado como pendente. |
| Legendas de figuras | Identificação da figura acima da imagem nas fontes examinadas; fonte/crédito abaixo quando informados | As três figuras do GuardKids têm identificação abaixo do desenho | Ajuste formal direto para aproximar a apresentação do exemplo: título acima, fonte abaixo. |
| Tabelas | Título acima; uso frequente de bordas e tabelas longas | Título acima; linhas horizontais com `booktabs` | Posição compatível. Copiar bordas e cores não é necessário para reproduzir a organização acadêmica. |
| Citações e referências | Usa `abntex2cite` e bibliografias `.bib` | Autor-data e referências foram digitados manualmente | A existência de citações não depende de usar um pacote. Automatizar melhora consistência e manutenção; a correspondência autor/ano/referência ainda precisa ser conferida. |
| Elementos de trabalho concluído | Ata assinada e ficha catalográfica próprias do autor | Não contém ata, nomes de banca ou ficha fictícios | Não importar documentos ou identidades do exemplo. A necessidade desses elementos decorre da etapa e de documentos reais do GuardKids. |
| Conclusão | Discute resultados alcançados e trabalhos futuros | Delimita verificação técnica e avaliação de conteúdo futura | Adequada à evidência atual de TCC I. Não deve adotar conclusão de eficácia somente porque o exemplo apresenta pesquisa concluída. |

## 4. Melhorias prioritárias identificadas

### P1 — Recuperar o desenvolvimento da fundamentação

**Local:** `texto/02_referencial.tex`.

O referencial do exemplo apresenta conceitos, seus componentes e sua ligação com os métodos implementados. No GuardKids, a discussão de trabalhos relacionados ocupa parte importante de um capítulo curto, enquanto o funcionamento e os limites dos mecanismos aparecem resumidos.

O aprofundamento deve explicar, com referências pertinentes:

1. O papel dos LLMs no chatbot e a distinção entre geração, instruções e classificação.
2. O que são guardrails de entrada e saída, como a política contextual altera o tratamento e como ocorrem falsas recusas.
3. Como embeddings, similaridade, seleção de passagens e geração com fontes se relacionam no RAG.
4. Por que correção factual, sustentação documental, segurança e atendimento educativo são propriedades diferentes.
5. Como os riscos de conteúdo e o perfil fictício se relacionam às categorias escolhidas.
6. Quais características dos trabalhos relacionados sustentam as escolhas do GuardKids e quais questões permanecem para seu recorte.

Isso pode aproveitar o material original preservado e as fontes já verificadas, seguido de revisão de coerência. Não implica restaurar afirmações de eficácia sem evidência nem adicionar assuntos sem relação com a pergunta de pesquisa. O critério de conclusão é o leitor compreender e avaliar as escolhas do artefato, não alcançar doze páginas.

### P1 — Mostrar evidências de desenvolvimento no próprio capítulo

**Local:** `texto/05_evidencias.tex`.

O exemplo aproxima descrição do método e saída obtida. O GuardKids dispõe de registros para fazer o mesmo no nível preliminar:

- Pergunta legítima apoiada e resposta efetiva.
- Pergunta de predação nas duas condições, incluindo bloqueio/redirecionamento observados.
- Pedido de ajuda e a orientação produzida.
- Caso de falta de apoio e a decisão de insuficiência.

Cada exemplo deve identificar caso, versão, condição, fontes e origem da decisão. A reprodução literal de uma resposta não equivale a julgamento humano de adequação. As conclusões sobre segurança, fidelidade e qualidade devem permanecer limitadas à evidência disponível. A avaliação final reservada não precisa ser executada para melhorar a demonstração dos testes de desenvolvimento já existentes.

### P1 — Descrever o ambiente das medições

**Local:** `texto/03_metodologia.tex` ou início do capítulo de evidências.

O exemplo informa o equipamento e as versões de software utilizados. O GuardKids já tem esses dados em `avaliacao/evidencias/ambiente_hardware.json`, nos snapshots e nos registros de modelos. A descrição no texto deve trazer o que afeta a inferência: processador, memória, GPU, sistema/versão de Python, serviço local e digests/versões dos modelos. Não se deve confundir a GPU disponível com execução comprovada integralmente em GPU, nem inferir VRAM a partir de um campo impreciso.

O critério de conclusão é permitir que o leitor interprete os tempos e identifique quais condições precisaria reproduzir.

### P2 — Separar visualmente os objetivos

**Local:** `texto/01_introducao.tex`.

Criar subseções para objetivo geral e objetivos específicos, mantendo os quatro objetivos existentes e sua correspondência com a matriz final. O exemplo facilita essa leitura. É uma melhoria de organização, não motivo para alterar o objetivo para uma avaliação final que ainda não foi realizada.

### P2 — Alinhar legendas e manutenção das citações

**Locais:** figuras nos capítulos de metodologia e artefato; `texto/referencias.tex` e citações no corpo.

Posicionar os títulos das três figuras acima dos desenhos, preservando fontes/créditos abaixo. Conferir títulos e chamadas nas listas. Para bibliografia, considerar `abntex2cite`/BibTeX com metadados das fontes realmente utilizadas, conferindo o PDF após a migração. Não copiar as referências de otimização do outro trabalho para ampliar artificialmente a bibliografia.

## 5. O que não deve ser copiado do exemplo

- Texto, resultados, equações, algoritmos, nomes, assinaturas e ficha catalográfica de outro autor.
- Datas de defesa ou afirmações de objetivos integralmente cumpridos que não correspondam ao GuardKids.
- O preâmbulo que alterna denominações institucionais no exemplo: a identificação do trabalho atual deve permanecer consistente.
- Comentários como “REVISAR” e instruções internas existentes nas fontes do modelo. Não fazem parte do texto acadêmico.
- Opções tipográficas antigas em conflito com as orientações aplicáveis à entrega atual.
- Tópicos que estão dentro de ambientes `comment` do LaTeX e não aparecem no PDF. A inspeção excluiu esses blocos das contagens auxiliares.

O PDF e a fonte do ZIP não são equivalentes em todos os detalhes visuais, como mostra a folha de rosto. O PDF foi usado como referência da apresentação efetivamente fornecida; as fontes serviram para identificar estrutura e escolhas técnicas.

## 6. Parecer final da comparação

**Base visual e estrutura:** compatíveis nos elementos principais, com ajustes formais identificados.

**Desenvolvimento acadêmico:** o referencial do GuardKids está substancialmente mais resumido; a demonstração dos resultados de desenvolvimento também pode ser ampliada usando evidências já existentes. Esses são os pontos mais relevantes para aproximar o trabalho da densidade do exemplo.

**Etapa da pesquisa:** o planejamento e a avaliação preliminar devem continuar identificados como TCC I. O estudo de 2018 não autoriza declarar concluída a avaliação humana do GuardKids.

**Prioridade prática:** aprofundar a teoria, apresentar exemplos reais de desenvolvimento e explicitar o ambiente experimental; depois ajustar objetivos, legendas e bibliografia. Aumentar páginas com elementos opcionais não resolve essas necessidades.

Esta validação gerou o presente relatório e dados de comparação. Não alterou o conteúdo do GuardKids, o protocolo, os casos, os resultados ou os documentos do autor da referência.

## 7. Rastreabilidade

- PDF de referência extraído: `.cache/validacao_unitins/referencia/tcc.pdf`.
- Ata lida visualmente: `.cache/validacao_unitins/referencia/anexos/AVALIACAO.pdf`.
- Fonte do exemplo: `.cache/validacao_unitins/referencia/`, com nomes e hashes em `comparacao_dados.json`.
- Dados de inspeção: `.cache/validacao_unitins/comparacao_dados.json`.
- Manual complementar: `avaliacao/fontes/manual_unitins.pdf`, especialmente páginas físicas 14, 16, 18 e 19; URL e SHA-256 em `avaliacao/fontes/downloads.json`.
- Páginas físicas usadas no quadro: exemplo, introdução 15–16, referencial 17–28, metodologia 29–43, resultados 44–52, conclusão 53–54; GuardKids, introdução 9–10, fundamentação 11–13, metodologia 14–17, artefato 18–22, evidências 23–25 e considerações finais 26–27.
