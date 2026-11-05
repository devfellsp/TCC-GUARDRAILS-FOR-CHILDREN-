# Auditoria do TCC GuardKids — quatro eixos

Base: projeto TCC-GUARDRAILS-FOR-CHILDREN--main; main.tex e arquivos incluídos; PDF TCC_GuardKids_Drawio_rotulos.pdf,41 páginas. Auditoria iniciada em4nov2026 e retomada após interrupções de limite de uso.

**Entrega de avaliação, sem alteração do manuscrito.** Foram examinados17 arquivos.tex,20 referências,7 figuras,11 tabelas,1 equação,1 algoritmo e registros de desenvolvimento. Há correções formais e de precisão a aplicar. Não foram encontrados erros nos totais dos lotes nem nas concordâncias destacadas pelo roteiro. As pendências documentais remanescentes estão identificadas, especialmente data da página Smithsonian e identificação editorial completa do volume SEDUC. Nenhuma pretensão de conformidade absoluta é feita.

As linhas são da versão auditada. Após aplicar alterações, podem mudar. Código LaTeX neste relatório é proposta; não foi compilado como alteração do TCC. A prova de preservação compara hashes dos fontes,figuras,PDFs eZIPs existentes.

## Eixo 1 — Gramática, regência, paralelismo e coesão

Foram lidos os 17 arquivos `.tex`: `main.tex`, `document.tex`, os 11 arquivos de `texto/` e os quatro de `generated/`. `texto/04_artefato.tex` integra o manuscrito por inclusão na linha 58 de `texto/03_metodologia.tex`. A verificação considera a redação corrente, sem modificar o projeto.

**Resultado:** não foi encontrado desvio inequívoco de concordância verbal/nominal ou crase nos casos destacados no pedido. Há construções truncadas, referentes imprecisos e coordenações pouco claras que devem ser corrigidas. Não se deve apresentar esses achados como uma lista de erros de concordância que o texto não contém.

### E1-01 — Explicitar o que é encerrado

**Moderado — `texto/04_artefato.tex`, linha 17.**

Original: “A falta de passagens encerra após classificação e embedding; insuficiência declarada pelo gerador e reprovação de sustentação encerram antes do classificador de saída.”

Diagnóstico: os verbos `encerra` e `encerram` deixam implícito o objeto, enquanto os sujeitos expressam condições de parada. A elipse dificulta distinguir o encerramento da geração do encerramento da tentativa inteira, que ainda deve passar pelo registro. A concordância singular/plural existente está correta; o problema é de completude e precisão da construção.

Buscar:
```latex
A falta de passagens encerra após classificação e embedding; insuficiência declarada pelo gerador e reprovação de sustentação encerram antes do classificador de saída.
```
Substituir:
```latex
A ausência de passagens interrompe o caminho de geração após a classificação da entrada e a geração do embedding da pergunta. A insuficiência declarada pelo gerador e a reprovação na verificação de sustentação também interrompem esse caminho antes da classificação da saída. Em todos esses casos, a tentativa segue para o registro da rota correspondente.
```

### E1-02 — Corrigir a predicação de “saídas finais”

**Moderado — `texto/05_evidencias.tex`, linha 25.**

Original: “Não houve ajuste dos prompts com base nas saídas finais, que continuam não executadas.”

Diagnóstico: a oração relativa retoma `saídas finais`, mas saídas são geradas; o que se executa é a avaliação ou o lote. É uma inadequação semântica entre sujeito e predicado, não falta de concordância.

Buscar:
```latex
Não houve ajuste dos prompts com base nas saídas finais, que continuam não executadas.
```
Substituir:
```latex
Não houve ajuste dos prompts com base em respostas da avaliação final, pois essa avaliação ainda não foi executada.
```

### E1-03 — Corrigir sujeito e paralelismo na descrição de latência

**Moderado — `texto/05_evidencias.tex`, linha 49.**

Original: “O caminho de geração pode executar quatro chamadas ao LLM, enquanto mensagens fixas podem encerrar após uma classificação ou detector local.”

Diagnóstico: mensagens não encerram o processamento; são resultados de uma rota. A coordenação `após uma classificação ou detector local` também mistura um procedimento com o componente que o realiza. Descrever os dois eventos no mesmo plano elimina a ambiguidade.

Buscar:
```latex
O caminho de geração pode executar quatro chamadas ao LLM, enquanto mensagens fixas podem encerrar após uma classificação ou detector local.
```
Substituir:
```latex
O caminho de geração pode executar quatro chamadas ao LLM. Nas rotas de mensagens fixas, a decisão de tratamento pode ser obtida após a classificação da entrada ou a detecção local de identificadores, sem percorrer todo o caminho de geração.
```

### E1-04 — Especificar em que consiste a assistência de IA

**Moderado — `texto/06_consideracoes.tex`, linha 20.**

Original: “Os enunciados são intencionais, conhecidos pelos autores e assistidos por IA; a reserva futura é operacional e compartilha conceitos com o desenvolvimento.”

Diagnóstico: `intencionais` não explicita a seleção intencional da amostra; `assistidos por IA` atribui a assistência aos enunciados, em vez de à atividade de elaborá-los. O paralelismo morfológico existe, mas as propriedades coordenadas têm referentes conceituais imprecisos.

Buscar:
```latex
Os enunciados são intencionais, conhecidos pelos autores e assistidos por IA; a reserva futura é operacional e compartilha conceitos com o desenvolvimento.
```
Substituir:
```latex
Os enunciados foram selecionados de forma intencional e elaborados com assistência de IA; são conhecidos pelos autores. O conjunto reservado tem caráter operacional e compartilha conceitos com o conjunto de desenvolvimento.
```

### E1-05 — Explicitar agentes, respostas e conjunto de desenvolvimento

**Moderado — `texto/06_consideracoes.tex`, linha 24.**

Original: “O conjunto reservado e o executor foram preparados após a inspeção do desenvolvimento, sem gerar suas respostas. Ajustes futuros do verificador de sustentação devem usar desenvolvimento e uma nova versão, preservando os registros atuais; mudanças motivadas por saídas finais exigirão novo planejamento.”

Diagnóstico: `sem gerar suas respostas` deixa indefinidos o agente da geração e o referente de `suas`, após um sujeito composto por conjunto e executor. `Usar desenvolvimento e uma nova versão` coordena objetos de natureza diferente e omite se se trata de dados, casos ou etapa de desenvolvimento. Não há erro na concordância de `foram preparados`.

Buscar:
```latex
O conjunto reservado e o executor foram preparados após a inspeção do desenvolvimento, sem gerar suas respostas. Ajustes futuros do verificador de sustentação devem usar desenvolvimento e uma nova versão, preservando os registros atuais; mudanças motivadas por saídas finais exigirão novo planejamento.
```
Substituir:
```latex
O conjunto reservado e o executor foram preparados após a inspeção dos resultados de desenvolvimento. As respostas às perguntas do conjunto reservado ainda não foram geradas. Ajustes futuros do verificador de sustentação devem ser realizados com casos de desenvolvimento e registrados em uma nova versão, preservando os registros atuais. Mudanças motivadas pelas saídas da avaliação final exigirão novo planejamento.
```

### E1-06 — Identificar quem confirma e quais dados são registrados

**Moderado — `texto/apendice_reproducao.tex`, linha 19.**

Original: “A referência em CSV aguarda confirmação, identidade, data e justificativa humanas.”

Diagnóstico: `humanas` concorda formalmente com a enumeração feminina, mas produz a combinação semanticamente imprópria `data humana`. A pessoa é responsável pela confirmação e pela justificativa; identidade e data são campos de registro. Explicitar essa relação é preferível à enumeração comprimida.

Buscar:
```latex
A referência em CSV aguarda confirmação, identidade, data e justificativa humanas.
```
Substituir:
```latex
A referência em CSV aguarda confirmação por um revisor humano, com registro de sua identidade, da data e da justificativa.
```

### E1-07 — Melhorar a construção verbal de conclusão das tentativas

**Refinamento — `texto/05_evidencias.tex`, linha 11.**

Original: “Todas concluíram sem perda técnica.”

Diagnóstico: o antecedente é `tentativas`. A formulação passiva identifica mais claramente o resultado do processamento e evita a leitura de que as tentativas praticam a ação de concluir. Não se trata de erro de número ou pessoa verbal.

Buscar:
```latex
Todas concluíram sem perda técnica.
```
Substituir:
```latex
Todas foram concluídas sem perda técnica.
```

### E1-08 — Aproximar o particípio de seu referente

**Refinamento — `texto/05_evidencias.tex`, linha 67.**

Original: “O piloto de 25 de outubro de 2026 contém 11 perguntas em duas condições, totalizando 22 execuções, associado ao código original identificado por \texttt{1c7e0b3}.”

Diagnóstico: `associado` concorda corretamente com `piloto`, mas a oração de gerúndio e os dois grupos numéricos distanciam o particípio do referente. Dividir o período facilita a leitura sem alterar o significado.

Buscar:
```latex
O piloto de 25 de outubro de 2026 contém 11 perguntas em duas condições, totalizando 22 execuções, associado ao código original identificado por \texttt{1c7e0b3}.
```
Substituir:
```latex
O piloto de 25 de outubro de 2026 está associado ao código original identificado por \texttt{1c7e0b3}. Contém 11 perguntas em duas condições, totalizando 22 execuções.
```

### E1-09 — Explicitar o substantivo nas células de situação

**Refinamento — `texto/06_consideracoes.tex`, linhas 13–14, `tab:objetivos`.**

Originais: “Realizado; sem julgamento humano de eficácia.” e “Preparado; ratificação e execução final pendentes.”

Diagnóstico: os particípios masculinos podem retomar `objetivo` ou um termo subentendido, portanto não é defensável afirmar erro obrigatório de concordância com `avaliação`. O problema é a ausência de um referente explícito e uniforme na coluna. As substituições abaixo tratam somente da redação; a correspondência entre esses objetivos e os objetivos da introdução precisa ser examinada no eixo de consistência.

Buscar:
```latex
Realizado; sem julgamento humano de eficácia.
```
Substituir:
```latex
Documentação concluída; sem julgamento humano de eficácia.
```

Buscar:
```latex
Preparado; ratificação e execução final pendentes.
```
Substituir:
```latex
Plano preparado; ratificação e execução final pendentes.
```

### E1-10 — Tornar inequívoca a enumeração dos três grupos

**Refinamento — `texto/04_artefato.tex`, linha 7.**

Original: “A Figura~\ref{fig:arquitetura} organiza os componentes em três grupos: entrada, processamento com fontes e verificação e entrega.”

Diagnóstico: a sequência de duas conjunções `e` torna pouco visível a fronteira entre o segundo e o terceiro grupo. Não é erro de concordância; a enumeração explícita melhora a leitura.

Buscar:
```latex
A Figura~\ref{fig:arquitetura} organiza os componentes em três grupos: entrada, processamento com fontes e verificação e entrega.
```
Substituir:
```latex
A Figura~\ref{fig:arquitetura} organiza os componentes em três grupos: (i) entrada; (ii) processamento com fontes; e (iii) verificação e entrega.
```

### E1-11 — Evitar repetição imediata da delimitação

**Refinamento — `texto/01_introducao.tex`, linhas 7 e 9.**

Originais: “Não há participantes infantis, observação de aprendizagem nem medição de compreensão por crianças.” e, no parágrafo seguinte, “A verificação preliminar concentra-se no comportamento técnico do sistema e não inclui avaliação de aprendizagem ou compreensão por crianças.”

Diagnóstico: a mesma delimitação é repetida em parágrafos consecutivos. Preservar integralmente a primeira ocorrência e concentrar a segunda no escopo técnico elimina redundância. Reiterações em capítulos distintos, quando necessárias para delimitar resultados e conclusões, não devem ser removidas indiscriminadamente.

Buscar:
```latex
A verificação preliminar concentra-se no comportamento técnico do sistema e não inclui avaliação de aprendizagem ou compreensão por crianças.
```
Substituir:
```latex
A verificação preliminar concentra-se no comportamento técnico do sistema.
```

### Construções verificadas que não devem ser marcadas como erro

| Construção | Local | Resultado |
|---|---|---|
| “prepararam-se 32 enunciados” | `main.tex:51` | Plural correto na passiva sintética. |
| “Consideraram-se publicações” | `texto/02_referencial.tex:7` | Plural correto. |
| “Segurança, decisão de tratamento, correção, fidelidade e linguagem são avaliadas separadamente.” | `texto/03_metodologia.tex:7` | Todos os núcleos são femininos; particípio feminino plural correto. |
| “preservaram-se as exclusões”; “não se importaram imagens nem páginas integrais” | `texto/03_metodologia.tex:28` | Verbos concordam com sujeitos pacientes plurais. |
| “Parte das fontes de conferência pertence” | `texto/03_metodologia.tex:28` | Concordância com o núcleo partitivo `parte` é correta. |
| “observaram-se respectivamente 20, 6 e 6 passagens” | `texto/03_metodologia.tex:56` | Plural correto; isolar `respectivamente` com vírgulas é escolha estilística, não correção obrigatória. |
| “Planejam-se 64 julgamentos”; “Apresentam-se contagens e denominadores” | `texto/03_metodologia.tex:96,106` | Plurais corretos. |
| “O protocolo, os casos, os modelos, o índice e as instruções devem ser congelados” | `texto/03_metodologia.tex:102` | Concordância no masculino plural correta para sujeito composto de gêneros diferentes. |
| “Não se somam as 32 tentativas atuais às 108 históricas” | `texto/03_metodologia.tex:112` | Plural e crase corretos. |
| “Trata-se de inspeção assistida” | `texto/05_evidencias.tex:19` | Singular correto; o complemento preposicionado não é sujeito. |
| “Foram apontadas ressalvas”; “cinco das oito explicações” | `texto/05_evidencias.tex:19` | Concordância correta; a expressão fracionária não cria erro no período. |
| “O conjunto reservado e o executor foram preparados” | `texto/06_consideracoes.tex:24` | Masculino plural correto. |
| “Planejam-se 64 pareceres primários e 16 secundários” | `texto/apendice_reproducao.tex:21` | Plural correto. |
| “quanto à correção, à sustentação e à clareza” | `texto/02_referencial.tex:72` | Regência e paralelismo preposicional corretos. |
| “em relação a um sistema” | `texto/01_introducao.tex:23` | Sem crase diante do artigo indefinido masculino. |
| “ausência de contradição não equivale a sustentação” | `texto/05_evidencias.tex:23` | Não há erro obrigatório: o substantivo abstrato pode ser empregado genericamente sem artigo; não inserir crase mecanicamente. |

Nos objetivos específicos de `texto/01_introducao.tex:38`, a sequência “explicitar”, “implementar e verificar”, “revisar [...] e comparar” e “preparar” mantém o paralelismo de infinitivos. A coluna de decisões em `tab:trabalhos` também o mantém: “Fixar”, “Examinar”, “Separar” e “Julgar”. As instruções do algoritmo usam infinitivos de maneira coerente; `verificados` na entrada do algoritmo concorda corretamente com a enumeração de gêneros diferentes. A condição abreviada `não sustentada` é compreensível no pseudocódigo e não deve ser anunciada como erro gramatical obrigatório.

A redação telegráfica de `tab:politicas` é compatível com células de tabela. Há oportunidade facultativa de tornar “Ajuda para recusar/procurar responsável” (`texto/04_artefato.tex:39`) mais explícito: `Pedido de ajuda para recusar o consumo ou procurar um responsável: orientar.` A barra atual comprime a relação entre as ações, mas não comprova erro de concordância.

As respostas de `generated/pilot_responses.tex` são transcrições de registros experimentais, conforme o comentário do próprio arquivo e a coluna “Resposta literal”. Eventuais problemas de redação ou de conteúdo nessas respostas devem ser analisados como evidência e preservados, não corrigidos no registro. As demais tabelas de `generated/` contêm rótulos e números, sem desvio sintático identificado. Padronização de separadores decimais pertence ao eixo de apresentação tabular.

### Prioridades do Eixo 1

| Prioridade | Itens | Encaminhamento |
|---|---|---|
| Crítico | Nenhum desvio linguístico classificado neste nível | Não inflar a gravidade de ajustes de redação. |
| Moderado | E1-01 a E1-06 | Corrigir sujeitos, objetos e referentes para descrever sem ambiguidade o fluxo e as etapas ainda pendentes. |
| Refinamento | E1-07 a E1-11 | Melhorar fluidez, retomadas e paralelismo sem alterar os dados. |


## Eixo 2 — Normas e apresentação

### E2-01 — Resumo e Abstract

Contagem por tokens separados por espaço, excluindo títulos e palavras-chave e mantendo palavras hifenizadas como uma unidade: **Resumo 237; Abstract 220**. Ambos estão em parágrafo único, sem citações, com quatro termos-chave. As informações numéricas e as ressalvas são equivalentes. Não há razão para cortar texto para atingir 150–250 palavras.

O manual institucional de 2025, §§7.1.5–7.1.7, prevê 150–250 palavras, quatro termos, fonte 10 ou 11 no resumo e títulos de elementos preliminares em maiúsculas, com as especificações de destaque de cada elemento. O texto atual usa o tamanho-base 12; o título do resumo e das listas mantém a apresentação padrão da classe. Isso exige ajuste de apresentação, não reescrita do conteúdo. [Manual UNITINS](https://www.unitins.br/cms/Arquivos/Download/D5D2798C96CF7CE88B0DBDD1CB2AE0174CC49043).

**Moderado — main.tex:50–61.** Originais: “\begin{resumo}”, “\begin{resumo}[Abstract]” e as linhas de palavras-chave com pontos. A NBR6028:2021, §4.1.7, estabelece separação por ponto e vírgula, minúsculas salvo nomes próprios, e ponto final. O manual não impõe pontos na seção específica da monografia; não transportar automaticamente regra do modelo de artigo. [NBR6028:2021](https://www5.unioeste.br/portalunioeste/arq/files/PGEAGRI/NBR6028.pdf).

Buscar → substituir:
~~~latex
% Buscar:
\begin{resumo}
% Substituir:
\begin{resumo}[RESUMO]
\fontsize{11}{13.2}\selectfont\SingleSpacing

% Buscar:
\begin{resumo}[Abstract]
% Substituir:
\begin{resumo}[ABSTRACT]
\fontsize{11}{13.2}\selectfont\SingleSpacing

% Buscar:
\textbf{Palavras-chave}: Guardrails. Chatbot educativo. Segurança infantil. Geração aumentada por recuperação.
% Substituir:
\textbf{Palavras-chave}: guardrails; chatbot educativo; segurança infantil; geração aumentada por recuperação.

% Buscar:
\textbf{Keywords}: Guardrails. Educational chatbot. Child safety. Retrieval-augmented generation.
% Substituir:
\textbf{Keywords}: guardrails; educational chatbot; child safety; retrieval-augmented generation.
~~~

A tipografia dos títulos também deve ser ajustada no estilo abnTeX2. Proposta a inserir no preâmbulo após unitins:
~~~latex
\renewcommand{\ABNTEXchapterfont}{\normalfont\bfseries}
\renewcommand{\ABNTEXchapterfontsize}{\normalsize}
\renewcommand{\resumoname}{RESUMO}
\addto\captionsbrazil{%
  \renewcommand{\listfigurename}{LISTA DE ILUSTRAÇÕES}%
  \renewcommand{\listtablename}{LISTA DE TABELAS}%
  \renewcommand{\contentsname}{SUMÁRIO}%
}
~~~
Este bloco afeta títulos e deve ser compilado e inspecionado em uma etapa posterior de aplicação. O fallback TeX Gyre Termes em main.tex:8 é semelhante à Times, mas não é literalmente Times New Roman. Caso a exigência institucional seja literal, deve-se fornecer uma fonte autorizada e configurar fontspec; não renomear a fonte para aparentar conformidade.

### E2-02 — Inventário de figuras, tabelas, equação e algoritmo

**Moderado: sete captions abaixo dos desenhos.** A identificação de ilustração deve ficar acima e sua fonte abaixo. Todos os sete desenhos possuem fonte e chamada prévia. O problema é a posição do título. [NBR14724, regras de ilustrações reproduzidas pela instituição](https://fatecjd.edu.br/docs/Informativo_ALTERA%C3%87%C3%95ES%20ABNT_Modelos%202023.pdf). Para versões atuais:14724:2024,10520:2023,6023:2025 e6028:2021. [Biblioteca UFES](https://biblioteca.ufes.br/normalizacao).

| Objeto | Arquivo e linha do rótulo | Chamada no código | Título/fonte |
|---|---|---|---|
| fig:dilema | 01_introducao:19 | Antes,15 | Título abaixo; fonte abaixo |
| fig:contexto | 02_referencial:25 | Antes,21 | Idem |
| fig:acervo | 03_metodologia:34 | Antes,30 | Idem |
| fig:protocolo | 03_metodologia:66 | Antes,62 | Idem |
| fig:arquitetura | 04_artefato:11 | Antes,7 | Idem |
| fig:percurso | 04_artefato:23 | Antes,19 | Idem |
| fig:decisao | 04_artefato:51 | Antes,7 e47 | Idem |
| tab:curriculo | 02_referencial:60 | Antes,57 | Correto |
| tab:trabalhos | 02_referencial:75 | Antes,72 | Correto |
| tab:corpus | 03_metodologia:18 | Depois,30 | Correto |
| tab:parametros | 03_metodologia:43 | Ausente | Correto |
| tab:amostra | 03_metodologia:83 | Antes,80 | Correto |
| tab:politicas | 04_artefato:32 | Depois,45 | Correto |
| tab:multichat | 05_evidencias:14 | Antes,11 | Correto |
| tab:lotes | 05_evidencias:36 | Antes,31 | Correto |
| tab:rotas | 05_evidencias:44 | Ausente | Correto |
| tab:objetivos | 06_consideracoes:8 | Antes,5; também introdução38 | Correto |
| tab:cronograma | 06_consideracoes:31 | Ausente | Correto |
| eq:ascs | 03_metodologia:108 | Antes,106 | Equação numerada; não requer caption/fonte de ilustração |
| alg:fluxo | 04_artefato:60 | Depois no código,80; antes no PDF atual devido à flutuação | Caption acima; sem indicação de autoria |

A posição no código não é necessariamente a posição no PDF. No PDF atual, a chamada ao algoritmo antecede sua exibição. Mover sua apresentação para antes do ambiente torna a ordem estável, mas não se deve anunciar uma inversão visual que não existe. As listas do PDF contêm sete figuras e onze tabelas.

Inserções prontas imediatamente antes do ambiente correspondente:
~~~latex
% texto/03_metodologia.tex, antes de tab:corpus:
A Tabela~\ref{tab:corpus} apresenta o conteúdo e a procedência dos trechos de cada chat.

% texto/03_metodologia.tex, antes de tab:parametros:
A Tabela~\ref{tab:parametros} reúne os parâmetros mantidos no lote de desenvolvimento.

% texto/04_artefato.tex, antes de tab:politicas:
A Tabela~\ref{tab:politicas} relaciona as categorias de proteção aos tratamentos previstos.

% texto/05_evidencias.tex, antes de tab:rotas:
A Tabela~\ref{tab:rotas} apresenta as rotas observadas em cada condição da versão GK-P1.2.

% texto/06_consideracoes.tex, antes de tab:cronograma:
A Tabela~\ref{tab:cronograma} distingue as etapas realizadas da continuidade proposta.

% texto/04_artefato.tex, antes do algoritmo:
O Algoritmo~\ref{alg:fluxo} sintetiza o processamento, distinguindo insuficiência de apoio, proteção e falha técnica.
~~~
No algoritmo, pode-se inserir imediatamente antes de \end{algorithm}:
~~~latex
\medskip
{\footnotesize Fonte: Elaboração própria a partir da implementação do GuardKids.\par}
~~~
A nova chamada não exige apagar a explicação posterior. Os blocos completos para reposicionar as sete captions estão ao final deste relatório.

### E2-03 — Siglas e apresentação numérica

**Moderado/refinamento — main.tex:68–79 e primeiras ocorrências no corpo.** A lista não substitui a expansão no texto. BNCC e PoC são introduzidas por extenso; RAG também. IA, JSON, LLM e ASCS requerem explicitação junto à primeira ocorrência relevante; TCC/UNITINS já possuem expansões nos elementos iniciais. SHA-256 está listado, mas não é utilizado como sigla no corpo: remover a entrada ou explicitar o algoritmo de hash onde for tecnicamente confirmado. Não inserir expansão em nomes de arquivos.

Buscar → substituir:
~~~latex
% texto/01_introducao.tex:5:
Grandes modelos de linguagem produzem
% por:
Grandes modelos de linguagem (\textit{large language models}, LLMs) produzem

% texto/02_referencial.tex:13:
princípios gerais de inteligência artificial
% por:
princípios gerais de inteligência artificial (IA)

% texto/03_metodologia.tex:28:
e à EJA,
% por:
e à Educação de Jovens e Adultos (EJA),

% texto/04_artefato.tex:80:
A API limita
% por:
A interface de programação de aplicações (API) limita

% texto/03_metodologia.tex:112:
Erros de modelo, prazo, JSON, índice ou persistência
% por:
Erros de modelo, prazo, formato \textit{JavaScript Object Notation} (JSON), índice ou persistência

% texto/apendice_reproducao.tex:7:
o CSV vincula
% por:
o arquivo de valores separados por vírgula (CSV) vincula
~~~
PDF pode ser apresentado na primeira ocorrência como “formato de documento portátil (PDF)”; IDs como “identificadores (IDs)” em04:15. SME/SEDUC são resolvidas pelas chamadas institucionais propostas. NIC.br deve ser expandido. MEC/MJSP/ACL/EMNLP/NAACL/CHI que aparecem somente em referências não exigem automaticamente uma entrada na lista de siglas do texto. URL é comando LaTeX, não necessariamente sigla impressa. Acrescentar EJA/API/CSV/PDF à lista é recomendável se usados repetidamente; não inflar a lista com comandos internos.

Em generated/development_summary.tex:3–4, originais “2.208”, “0.678 a 24.257”, “2.500” e “0.710 a 11.235”: padronizar separador decimal português, preservando arredondamento:
~~~latex
GK-P1.1 & 27 / 54 & 0 & 2,208 & 0,678 a 24,257 \\
GK-P1.2 & 27 / 54 & 0 & 2,500 & 0,710 a 11,235 \\
~~~
A geração futura da tabela deve conservar esse formato; não alterar os valores brutos experimentais.




### E2-R — Correspondência entre as 20 referências e o manuscrito

O arquivo texto/referencias.tex contém **20 entradas**, nas linhas 5 a 43, e não 19. “Correspondência 1 para 1” foi interpretada como rastreabilidade nos dois sentidos: toda obra utilizada deve ser identificável na lista e toda entrada deve ter uso identificável. Uma obra pode naturalmente ser citada várias vezes.

| Entrada e linha em referencias.tex | Chamada identificada | Diagnóstico |
|---|---|---|
| Brasil/MEC, BNCC, 2018 — 5 | 02_referencial.tex:57,81 | Correspondência explícita. |
| Brasil/MJSP, guia, 2025 — 7 | 02_referencial.tex:19,26 | Correspondência explícita; conferir título pela folha de rosto, conforme Eixo 3. |
| Chen et al., 2024 — 9 | 02_referencial.tex:41,80 | Correspondência explícita; variante de prenome na fonte primária, conforme Eixo 3. |
| Gao et al., 2023 — 11 | 02_referencial.tex:45,80 | Correspondência explícita. |
| Goiânia, legenda — 13 | 03_metodologia.tex:23, menção coletiva à SME | Não há chamada que individualize esta obra e sua data. |
| Goiânia, paisagem — 15 | 03_metodologia.tex:23, menção coletiva à SME | Mesmo problema. |
| Goiânia, trabalho — 17 | 03_metodologia.tex:23, menção coletiva à SME | Mesmo problema. |
| Goiânia, objetos — 19 | 03_metodologia.tex:22, menção coletiva à SME | Mesmo problema. |
| Goiânia, fontes históricas — 21 | 03_metodologia.tex:22, menção coletiva à SME | Mesmo problema. |
| Inan et al., 2023 — 23 | 02_referencial.tex:33,79 | Correspondência explícita. |
| Khoo, Chua e Shong, 2025 — 25 | 02_referencial.tex:15,78 | Correspondência explícita. |
| Lewis et al., 2020 — 27 | 02_referencial.tex:39,80 | Correspondência explícita; entrada bibliográfica incompleta. |
| Núcleo de Informação e Coordenação do Ponto BR — 29 | 03_metodologia.tex:24, “NIC.br” | Uso identificável, mas sem autor-data; data da página recuperada: 2021. |
| Rath et al., 2025 — 31 | 01_introducao.tex:5; 02_referencial.tex:15,78 | Correspondência explícita. |
| Rebedea et al., 2023 — 33 | 02_referencial.tex:33,79 | Correspondência explícita. |
| São Paulo (Estado), 2024 — 35 | 03_metodologia.tex:21, “SEDUC-SP (2024)” | Ano presente; chamada não coincide com a entrada jurisdicional adotada. |
| São Paulo (Município), 2021 — 37 | 03_metodologia.tex:21, “SME-SP (2021)” | Mesmo problema de normalização da autoria. |
| Smithsonian Institution — 39 | 03_metodologia.tex:24, “Smithsonian” | Uso identificável, sem autor-data. |
| Volodina e Weinert, 2020 — 41 | 02_referencial.tex:53,81 | Correspondência explícita. |
| Wang et al., 2022 — 43 | 01_introducao.tex:5; 02_referencial.tex:13,78 | Correspondência explícita. |

São **11 entradas com chamada autor-data explícita**, duas chamadas abreviadas paulistas que precisam de normalização e sete fontes documentais sem chamada autor-data individualizada. Não se encontrou uma citação autor-data de obra científica ausente da lista. Também não é correto dizer que as nove fontes documentais “não foram usadas”: a tabela e o manifesto evidenciam sua utilização; falta formalizar a ligação bibliográfica no manuscrito.

**E2-R01 — Moderado.** Em texto/03_metodologia.tex:21, original: “SME-SP (2021) e SEDUC-SP (2024)”.

Buscar:
~~~latex
SME-SP (2021) e SEDUC-SP (2024).
~~~
Substituir:
~~~latex
São Paulo (Município, 2021) e São Paulo (Estado, 2024).
~~~
Essa opção mantém a autoria jurisdicional das referências. Não inserir caixa alta integral nas chamadas parentéticas por automatismo: a NBR 10520:2023 adota maiúsculas e minúsculas.

**E2-R02 — Moderado.** Em texto/03_metodologia.tex:22–24, originais: “materiais da SME de Goiânia”, “sombra conferida no Smithsonian” e “cuidados com dados no NIC.br”. Falta associar cada conjunto de conceitos às obras individuais. Aplicar conjuntamente as chamadas propostas e os tratamentos de datas abaixo; não mudar somente a tabela.

Uma solução documental conservadora é manter a autoria institucional de Goiânia e indicar década conhecida, sem inventar anos específicos. O portal oficial declara criação em 2020, e as cinco páginas já estavam disponíveis na auditoria de 2026; portanto **[202-] é uma inferência delimitada para a publicação no portal, não a transcrição de um ano expresso em cada aula**. Letras distinguem as cinco entradas na ordem alfabética dos títulos atualmente adotados. Se os títulos ou as autorias forem alterados, recalcular as letras. [Histórico oficial do Conexão Escola](https://sme.goiania.go.gov.br/conexaoescola/gestao_conteudo/sobre-o-portal-conexao-escola/).

Para Smithsonian, a ausência de data exata deve ficar explícita. Uma data aproximada só pode ser inserida com base documental; a referência proposta no Eixo 3 especifica o limite desta verificação. Não usar o ano de acesso como ano de publicação, nem transformar a data de um vídeo relacionado na data da página.

Para as cinco entradas de Goiânia, substituir, individualmente, “Conexão Escola. Disponível em:” por:
~~~latex
% linha 13: legenda
Conexão Escola, [202-]a. Disponível em:
% linha 15: paisagem
Conexão Escola, [202-]b. Disponível em:
% linha 17: trabalho
Conexão Escola, [202-]c. Disponível em:
% linha 19: objetos
Conexão Escola, [202-]d. Disponível em:
% linha 21: fontes históricas
Conexão Escola, [202-]e. Disponível em:
~~~

Buscar, em texto/03_metodologia.tex:
~~~latex
Conferência conceitual em materiais da SME de Goiânia.
~~~
Substituir:
~~~latex
Conferência conceitual em materiais da Secretaria Municipal de Educação de Goiânia (Goiânia, [202-]d, [202-]e).
~~~

Buscar:
~~~latex
Paisagem, legenda e relações campo-cidade; materiais da SME de Goiânia.
~~~
Substituir:
~~~latex
Paisagem, legenda e relações campo-cidade; materiais da Secretaria Municipal de Educação de Goiânia (Goiânia, [202-]a, [202-]b, [202-]c).
~~~

A inferência de década resolve a ausência de data sem atribuir precisão inexistente. A opção por autores pessoais, também identificados nas páginas, exige refazer simultaneamente entradas e chamadas; não misturar os dois sistemas.

**E2-R03 — Moderado.** Em texto/referencias.tex:29, original: “Cidadão na Rede. Disponível em:”. A própria página informa postagem em 20/07/2021. [Página do NIC.br](https://cidadaonarede.nic.br/pt/videos/seguranca/cuide-de-seus-dados-pessoais).

Buscar:
~~~latex
Cidadão na Rede. Disponível em:
~~~
Substituir:
~~~latex
Cidadão na Rede, 20 jul. 2021. Disponível em:
~~~

Buscar, em texto/03_metodologia.tex:24:
~~~latex
cuidados com dados no NIC.br.
~~~
Substituir:
~~~latex
cuidados com dados no Núcleo de Informação e Coordenação do Ponto BR (2021).
~~~

### E2-R04 — Autores, destaque e uniformidade da lista

A NBR 6023:2025 mantém, nos itens 8.1.1.1 e 8.1.1.2, a indicação de todos os autores quando são até três e a possibilidade de indicar todos ou somente o primeiro seguido de et al. quando são quatro ou mais. O segundo item **não contém literalmente** a condição “desde que haja uniformidade em toda a lista”, apresentada no roteiro como se fosse parte de sua redação. A uniformização editorial é recomendável, mas não se deve transformar uma das alternativas permitidas em erro isolado. A norma também exige consistência no destaque dos títulos (item 6.7). Para datas não localizadas, o item 8.6.1.3 prevê indicação entre colchetes; [S. l.] e [s. n.] tratam de local e editor, e não substituem uma data. [NBR 6023:2025, itens citados](https://bkpsitecpsnew.blob.core.windows.net/uploadsitecps/sites/149/2025/05/Referencias-NBR-6023-2025.pdf).

**Não há incoerência em “Khoo, Chua e Shong (2025)” versus “Rath et al. (2025)”**: são três autores no primeiro caso e quatro no segundo. A forma resumida no corpo não obriga a abreviar a lista de referências. Aplicar um padrão por escolha editorial, sem inventar autores nem omitir os três de MinorBench.

Padrão proposto para todas as 20 entradas: conservar as autorias institucionais já escolhidas; manter ambos os autores de Volodina/Weinert e os três de MinorBench; usar primeiro autor seguido de \textit{et al.} nas sete obras de quatro ou mais autores; manter título do periódico/anais em negrito nas partes de publicações, e título da própria obra em documentos autônomos. Verificar os metadados específicos no Eixo 3.

| Entrada | Ação de padronização |
|---|---|
| BNCC | Manter autoria institucional, título em negrito e ano. p. 339 já está na chamada; pode permanecer como localização do trecho consultado. |
| Guia MJSP | Manter institucional; corrigir ordem dos termos do título pela folha de rosto. |
| Chen | Conservar a variante Jianlyu dos metadados ACL ou declarar adoção da grafia Jianlv do PDF; usar \textit{et al.}; anais em negrito. |
| Gao | Trocar os quatro nomes por GAO, Tianyu \textit{et al.}; manter título do artigo sem destaque e anais em negrito. |
| Goiânia — legenda | Manter institucional; inserir data aproximada fundamentada e sufixo a. |
| Goiânia — paisagem | Idem, sufixo b; conferir transcrição do título na fonte. |
| Goiânia — trabalho | Idem, sufixo c. |
| Goiânia — objetos | Idem, sufixo d. |
| Goiânia — fontes | Idem, sufixo e. |
| Inan | Usar \textit{et al.}; preservar título destacado, condição de preprint, ano e arXiv. |
| MinorBench | Manter três nomes; fixar URL v1 se essa é a versão citada. |
| Lewis | Usar \textit{et al.}; retirar destaque do título do artigo e completar publicação/volume/páginas. |
| NIC.br | Manter institucional; inserir data efetiva de postagem. |
| Rath | Usar RATH, Prasanjit \textit{et al.}; explicitar título dos anais e local/editora. |
| Rebedea | Usar \textit{et al.}; explicitar título dos anais e local/editora. |
| São Paulo (Estado) | Preservar distinção jurisdicional; conferir título completo do volume e acesso documental. |
| São Paulo (Município) | Preservar distinção jurisdicional, edição e URL. |
| Smithsonian | Identificar data aproximada ou manter pendência explícita; não inventar ano exato. |
| Volodina/Weinert | Manter dois nomes, periódico em negrito, volume/artigo/DOI. |
| Wang | Usar WANG, Ge \textit{et al.}; manter anais em negrito e art. 536. |

Trocas editoriais prontas, exclusivamente em texto/referencias.tex:

~~~latex
% Buscar:
CHEN, Jianlyu et al.
% Substituir (mantém a grafia dos metadados ACL):
CHEN, Jianlyu \textit{et al.}

% Buscar:
GAO, Tianyu; YEN, Howard; YU, Jiatong; CHEN, Danqi.
% Substituir:
GAO, Tianyu \textit{et al.}

% Buscar:
INAN, Hakan et al.
% Substituir:
INAN, Hakan \textit{et al.}

% Buscar:
LEWIS, Patrick et al.
% Substituir:
LEWIS, Patrick \textit{et al.}

% Buscar:
RATH, Prasanjit; SHRAWGI, Hari; AGRAWAL, Parag; DANDAPAT, Sandipan.
% Substituir:
RATH, Prasanjit \textit{et al.}

% Buscar:
REBEDEA, Traian et al.
% Substituir:
REBEDEA, Traian \textit{et al.}

% Buscar:
WANG, Ge; ZHAO, Jun; VAN KLEEK, Max; SHADBOLT, Nigel.
% Substituir:
WANG, Ge \textit{et al.}
~~~

Não substituir nomes globalmente no corpo do texto ou dentro dos títulos. As trocas de metadados do Eixo 3 e estas trocas editoriais devem ser consolidadas antes de aplicar; não executar dois blocos concorrentes sobre a mesma referência.




## Eixo 3 — Verificação factual das fontes

As 12 categorias do pedido abrangem 20 entradas bibliográficas. A confirmação abaixo separa existência, fidelidade conceitual e precisão editorial. Não equivale a certificar todos os metadados como “100% corretos”.

| Fonte e passagem do TCC | Existência e metadados | Fidelidade e nuance |
|---|---|---|
| 1.Wang; 02:13, “correspondência entre princípios gerais [...] e orientações de design apropriado à idade” | Ge Wang, Jun Zhao, Max Van Kleek e Nigel Shadbolt; CHI2022,art536,1–29; DOI confere | Síntese compatível. Os exemplos de cuidado do GuardKids são aplicação do autor, não resultado experimental infantil de Wang. [Registro dos autores em Oxford](https://www.oxfordmartin.ox.ac.uk/publications/informing-age-appropriate-ai-examining-principles-and-practices-of-ai-for-children). |
| 2.Rath; 02:15, “avaliar seis modelos de linguagem” | Quatro autores da entrada conferem; NAACL2025,vol3 Industry,809–821; DOI confere | São efetivamente seis LLMs; perfis simulados informados por literatura de psicologia/cuidado infantil. Não implica testes com seis grupos de crianças. [ACL](https://aclanthology.org/2025.naacl-industry.62/). |
| 3.MinorBench; 02:15, “estudo de caso em ambiente escolar” | Shaun Khoo,Gabriel Chua,Rachel Shong; arXiv2503.10242v1,13mar2025; título confere | Contexto escolar real é confirmado; benchmark avalia recusa de solicitações arriscadas/inadequadas. Fixar URLv1. [arXiv](https://arxiv.org/abs/2503.10242v1). |
| 4.NeMo; 02:33, “programar restrições ao comportamento” | Traian Rebedea e quatro coautores; EMNLP2023 System Demonstrations,431–445; DOI confere | Fiel; biblioteca de controles programáveis. O TCC não afirma tê-la instalado. [ACL](https://aclanthology.org/2023.emnlp-demo.40/). |
| 5.Llama Guard; 02:33, “classificar entradas e respostas segundo categorias de segurança” | Hakan Inan e dez coautores;2023; arXiv2312.06674 | Fiel; modelo ajustado por instruções para classificação de prompts/respostas. Não transfere desempenho para Qwen3. [arXiv](https://arxiv.org/abs/2312.06674). |
| 6.Lewis; 02:39, “informação incorporada aos parâmetros [...] memória externa” | Obra real; NeurIPS2020,vol33,9459–9474. Entrada atual incompleta | Formulação paramétrica/não paramétrica fiel. Número33 é volume, não ordinal do evento. [Anais oficiais](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). |
| 7.Chen; 02:41, “BGE-M3, que admite diferentes formas de recuperação” | Findings ACL2024,2318–2335, DOI correto; seis autores | Densa, esparsa e multivetor confirmadas. Usar só densa é escolha da PoC. Metadados trazem Jianlyu; PDF traz Jianlv: variante real, não autor inventado. [ACL](https://aclanthology.org/2024.findings-acl.137/). |
| 8.Gao; 02:45, “fluência, correção e qualidade das citações” | Tianyu Gao,Howard Yen,Jiatong Yu,Danqi Chen;EMNLP2023,6465–6488;DOI correto | O texto atual está fiel. “Utilidade”, presente no roteiro do usuário, não é o nome da dimensão no TCC nem deve substituir “correção”. [ACL](https://aclanthology.org/2023.emnlp-main.398/). |
| 9.Volodina/Weinert; 02:53, “coortes entre o segundo e o quarto ano” | Anna Volodina e Sabine Weinert;Frontiers Psychology11,art814,2020;DOI confere | Alemanha,627 estudantes; duas coortes acompanhadas2º→3º e3º→4º, ligadas analiticamente. Não são todos os alunos acompanhados2º→4º. Ressalva sobre não validar estilo brasileiro está correta. [Artigo original](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00814/full). |
| 10.BNCC; 02:57, “EF04CI04” e “EF04CI06” | Documento2018; página impressa339, física341 no PDF consultado | Códigos e conteúdo corretos: cadeias/Sol e decomposição/fungos/bactérias. Não confundir numeração impressa e contador do leitor. [MEC](https://basenacionalcomum.mec.gov.br/images/BNCC_EI_EF_110518_versaofinal_site.pdf). |
| 11.ClassInd; 02:19, “descritores [...] contexto de apresentação” | 5ªed2025 confirmada; URL oficial válida; título da folha de rosto difere da ordem dos termos da landing | Uso como vocabulário de risco é fiel e explicitamente adaptado; não é certificação oficial do chatbot. [PDF MJSP](https://www.gov.br/mj/pt-br/assuntos/seus-direitos/classificacao-1/classind-audio-visual-2025-vs-10-nova-faixa.pdf). |

### 12 — Acervo curricular, fonte por fonte

| Fonte | Verificação e limite |
|---|---|
| Goiânia: legenda | Página existe e explica símbolos/cores, destinada ao3ºano. Título singular “A legenda do mapa” está correto apesar do slug plural. [Fonte](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/geografia-a-legenda-dos-mapas/). |
| Goiânia: paisagem | Distingue paisagem natural/cultural. Título atual é compatível. [Fonte](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/nocoes-de-paisagem-natural-e-cultural/). |
| Goiânia: trabalho | Trabalho, profissões e interdependência;4ºano. [Fonte](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/geografia-o-trabalho-e-os-trabalhadores/). |
| Goiânia: objetos | Objetos e memória histórica;2ºano. [Fonte](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/historia-cada-objeto-conta-uma-historia/). |
| Goiânia: fontes | Tipos de fontes históricas;4ºperíodo EJA, não4ºano infantil. O TCC já ressalva uso de fontes de outros anos/EJA em03:28. [Fonte](https://sme.goiania.go.gov.br/conexaoescola/eaja/historia-tipos-de-fontes-historicas/). |
| SME São Paulo2021 | Livro4ºano,vol2,2ªed,2021 confirmado. Página154 impressa corresponde à156 física; tema de cadeias alimentares compatível. [Livro oficial](https://acervodigital.sme.prefeitura.sp.gov.br/wp-content/uploads/2021/10/4ano_TA2_2ed_web.pdf). |
| SEDUC São Paulo2024 | Conteúdo local e páginas conferidos na etapa anterior da auditoria; volume reúne também Língua Inglesa e Tecnologia & Inovação. Não se localizou URL oficial inequívoca da mesma edição nem ano editorial explícito;2024 é sustentado por marcas técnicas do arquivo. Metadados editoriais permanecem pendentes, não certificados. |
| Smithsonian | URL existe; título mostrado: “Topics: light that does not pass”. Explica bloqueio de luz e sombras. “Shadows” identifica a URL/tema, não reproduz o título. Ano exato não confirmado. [Página](https://hte.si.edu/shadows.html). |
| NIC.br | Página existe, conteúdo sobre exposição de dados; postagem20/07/2021. Corrigir ausência de ano, conforme E2-R03. [Página](https://cidadaonarede.nic.br/pt/videos/seguranca/cuide-de-seus-dados-pessoais). |

### Correções bibliográficas e nuance prontas

**Moderado — referencias.tex:7.** Original “Guia Prático de Audiovisual, RPG e aplicativos”. A folha de rosto tem outra ordem. Buscar → substituir:
~~~latex
Guia Prático de Audiovisual, RPG e aplicativos
~~~
~~~latex
Guia Prático de Audiovisual, Aplicativos e RPG
~~~

**Moderado — referencias.tex:27.** Original “In: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS, 33., 2020.” Corrigir publicação/volume e deslocar o destaque:
~~~latex
LEWIS, Patrick \textit{et al.} Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In: \textbf{Advances in Neural Information Processing Systems}. [S. l.]: Curran Associates, 2020. v. 33, p. 9459--9474. Disponível em: \url{https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html}. Acesso em: 4 nov. 2026.
~~~

**Refinamento — referencias.tex:25.** Buscar URL:
~~~latex
https://arxiv.org/abs/2503.10242
~~~
Substituir:
~~~latex
https://arxiv.org/abs/2503.10242v1
~~~

**Moderado — referencias.tex:39.** Original “Here. There. Everywhere.: shadows”. Buscar → substituir:
~~~latex
Here. There. Everywhere.: shadows
~~~
~~~latex
Here. There. Everywhere.: light that does not pass
~~~
A data permanece pendente de identificação documental. Não preencher com2013 apenas porque um vídeo relacionado foi publicado naquele ano. A correção definitiva da chamada Smithsonian depende da data fundamentada. Esta pendência impede declarar conformidade bibliográfica integral.

**Moderado — referencias.tex:35.** Original “Currículo em Ação: Livro do Estudante: Ciências, Geografia e História”. A identificação completa deve ser confrontada com o exemplar; proposta compatível com a folha de rosto local:
~~~latex
SÃO PAULO (Estado). Secretaria da Educação. \textbf{Livro do Estudante: Ciências, Geografia, História, Língua Inglesa e Tecnologia \& Inovação: 4\textordmasculine{} ano, volume 2, 2\textordmasculine{} bimestre}. São Paulo: SEDUC-SP, [2024].
~~~
[2024] registra inferência, não ano editorial explicitamente impresso. Se adotado, alinhar a chamada para São Paulo (Estado, [2024]). A URL exata permanece pendente; não acrescentar um endereço de volume semelhante.

**Refinamento — 02_referencial.tex:53.** Original “acompanhando coortes entre o segundo e o quarto ano”. Não é erro demonstrado, mas pode ser mais preciso. Substituir somente esse trecho:
~~~latex
acompanhando duas coortes, uma do segundo ao terceiro ano e outra do terceiro ao quarto ano, articuladas em um desenho sequencial de coortes
~~~

Rath, Rebedea e Wang podem ter os títulos completos dos anais em lugar de “Proceedings [...]”, por padronização, sem alterar DOI/paginação. Não se encontrou artigo inexistente entre os nove estudos científicos examinados. A incerteza restante concentra-se na descrição bibliográfica de materiais documentais e não justifica acusação de fabricação de referências.




## Eixo 4 — Consistência interna e metodologia

### Conferência dos dados

Recalculei os CSVs e os instrumentos, sem depender exclusivamente dos resumos JSON.

| Conjunto | Resultado da conferência |
|---|---|
| Atual GK-P2.1-dev | 32 linhas,16 perguntas,16 tentativas por estilo. Totais:8 liberações+6 bloqueios+10 orientações+8 insuficiências=32. Zero perdas. Todos os campos humanos vazios. |
| Ressalvas atuais | Cinco avaliações assistidas de sustentação parcial: mc-g01,mc-h01,mc-c01 no Passo a passo e mc-d01 em ambos os estilos. Confere1 Direto+4 Passo a passo. As oito respostas vêm de quatro perguntas educativas. |
| GK-P1.1 | 54 registros,27 perguntas,27 por condição,zero perdas. Cada condição:5 allow,15 block,4 safe_guidance,3 redirect. |
| GK-P1.2 | 54 registros,27 perguntas. Referência:2+14+9+2=27. Ajustada:5+10+9+3=27. Confere com tabela. |
| Histórico total |27×2×2=108 execuções sobre as mesmas27 perguntas; não108 perguntas distintas. |
| Piloto1c7e0b3 |22 objetos em pilot_evidence.json,11 perguntas distintas,11 registros por condição,todos válidos; commit confere. |
| Plano final |casos.json tem32 enunciados em16 famílias,duas variantes cada; agenda64 entradas,32 por estilo. |
| Pareceres |CSV primário64 linhas,secundário16; agenda seleciona16 para segunda revisão.80×1–3min=80–240min. Leitura de fontes e conciliação estão fora da estimativa, como o texto informa. |
| Calibração |Recontagem27 casos:20 passagens em0,35;6 em0,45;6 em0,55. Não prova ótimo. |

Fontes: avaliacao/evidencias/multichat_20261104_revisado/resultados.csv e revisao_assistida_IA.json; CSVs dos dois diretórios desenvolvimento_20261103_*; poc/docs/pilot_evidence.json; avaliacao/final_multichat_v1/casos.json, agenda_planejada.json, parecer_primario.csv e parecer_secundario.csv. Os resultados calculados foram preservados em AUDITORIA_CALCULOS.json junto a este relatório.

A evolução dos seis casos de ajuda também confere: na GK-P1.1, cinco foram bloqueados e um orientado em cada condição; na GK-P1.2, seis orientados em cada condição. Nenhum número desses lotes precisa ser corrigido.

### E4-01 — Denominador ASCS ainda precisa de regra operacional

**Moderado — texto/03_metodologia.tex:106–112.**

Original: “saídas educativas com julgamento conclusivo nas dimensões”.

Diagnóstico: não está inequívoco se “saídas educativas” inclui recusas a perguntas educativas nem como se tratam dimensões não aplicáveis. A definição pode mudar o denominador. Não há taxa final errada calculada: o texto mantém taxas pendentes e prevê atendimento por oportunidade. A correção é explicitar a pendência antes de congelar o protocolo.

Buscar:
~~~latex
Para perguntas educativas, o atendimento seguro, correto e sustentado é definido na Equação~\ref{eq:ascs}; a clareza é relatada separadamente.
~~~
Substituir:
~~~latex
Para perguntas educativas, o atendimento seguro, correto e sustentado (ASCS) é definido na Equação~\ref{eq:ascs}; a clareza é relatada separadamente. Antes da avaliação final, o protocolo deve explicitar a unidade de contagem e os critérios de inclusão no denominador, inclusive o tratamento de recusas, julgamentos inconclusivos e dimensões não aplicáveis. O atendimento por oportunidade planejada será apresentado separadamente, conforme o tratamento das perdas descrito a seguir.
~~~
Essa redação não substitui a decisão metodológica nem autoriza alterar retroativamente rótulos. A regra escolhida precisa ser documentada antes da execução final.

### E4-02 — Correspondência entre objetivos e tabela de conclusão

**Moderado — texto/06_consideracoes.tex:11,13, confrontado com01_introducao.tex:38.**

Originais: “Explicitar proteção e acervo” e “Documentar desenvolvimento”. O objetivo(c) exige revisar acervos e comparar estilos; a tabela omite essas duas ações no rótulo da terceira linha. A primeira mistura(a) e parte de(c).

Buscar:
~~~latex
Explicitar proteção e acervo & Regra comum e oito trechos em quatro chats & Revisão documental assistida realizada; revisão humana pendente. \\
~~~
Substituir:
~~~latex
Explicitar a regra contextual & Regra comum para conteúdo educativo, risco, ajuda e falta de apoio & Regra documentada e implementada. \\
~~~

Buscar:
~~~latex
Documentar desenvolvimento & 32 tentativas atuais e 108 históricas separadas & Realizado; sem julgamento humano de eficácia. \\
~~~
Substituir:
~~~latex
Revisar acervos e comparar estilos no desenvolvimento & Revisão documental assistida; 32 tentativas nos dois estilos e inspeção das respostas; 108 registros históricos separados & Revisão e comparação preliminares realizadas; julgamento humano pendente. \\
~~~
Esta substituição integral prevalece sobre o refinamento isolado de “Realizado” em E1-09.

### E4-03 — Índice do lote versus prontidão da cópia

**Refinamento — texto/03_metodologia.tex:15 e apendice_reproducao.tex:11.**

Original: “O índice atual contém oito trechos”. O apêndice já informa ausência do ponteiro poc/data/current.json na cópia examinada, confirmada nesta auditoria. Isso não invalida o lote registrado, mas a expressão “atual” pode sugerir prontidão local.

Buscar:
~~~latex
O índice atual contém oito trechos: cinco recortes didáticos de Ciências e três sínteses autorais experimentais, uma por novo chat.
~~~
Substituir:
~~~latex
O índice utilizado no lote multidisciplinar de desenvolvimento contém oito trechos: cinco recortes didáticos de Ciências e três sínteses autorais experimentais, uma para cada um dos chats de História, Geografia e Geral. A prontidão da cópia local e o procedimento de reconstrução são descritos no Apêndice~\ref{ap:reproducao}.
~~~
Em02_referencial.tex:65, “recortes do índice ativo” pode ser substituído por “recortes do índice utilizado no lote de desenvolvimento”.

### E4-04 — Síntese geral ainda menciona somente dois lotes

**Moderado — texto/05_evidencias.tex:73.**

Original: “No funcionamento técnico, há código executável, testes aprovados, dois lotes completos e identificação dos componentes.”

Diagnóstico: a síntese geral não distingue os dois lotes históricos do lote atual adicional. Não é preciso mudar denominadores; basta explicitar a abrangência.

Buscar o período original e substituir:
~~~latex
No funcionamento técnico, há código executável, testes aprovados, dois lotes históricos de Ciências e um lote multidisciplinar de desenvolvimento concluídos, com identificação dos componentes; o piloto anterior é documentado separadamente.
~~~

### Limites metodológicos preservados

Não foi identificada promessa de aprendizagem/compreensão infantil medida, certificação pedagógica concluída ou ganho causal de segurança. O texto declara ausência de crianças participantes, proteção fixa, revisão humana pendente, reserva operacional e dependência entre paráfrases. Não acusar a pesquisa de apresentar um teste externo cego que ela explicitamente nega ter realizado.

As cinco ressalvas de sustentação são julgamentos assistidos pendentes de ratificação. Não convertê-las em cinco erros humanos certificados. A comparação de estilos é preliminar. Não somar32,108 e64 para construir indicador de eficácia.

## Tabela consolidada de prioridades

| Prioridade | Achados | Ação |
|---|---|---|
| Crítico | Nenhum erro crítico de cálculo, referência científica inexistente ou fabricação de avaliação humana foi demonstrado | Não inflar gravidade nem emitir certificado de ausência absoluta de erros. |
| Moderado | E2-R01–03: chamadas documentais incompletas; datas ausentes | Alinhar tabela e20 referências; resolver Smithsonian e edição SEDUC. |
| Moderado | Eixo3: título MJSP, entrada Lewis e identificação documental SEDUC/Smithsonian | Corrigir metadados verificáveis; conservar pendências explícitas. |
| Moderado | E2-01–02: títulos das7 figuras abaixo, chamadas faltantes/tardias, apresentação dos resumos | Ajustar LaTeX e verificar novo PDF. |
| Moderado | E4-01: denominador ASCS | Formalizar regra no protocolo antes da avaliação final. |
| Moderado | E4-02,04: objetivos e síntese de lotes | Corrigir redação sem mudar dados. |
| Moderado | E1-01–06: sujeitos/objetos e referentes imprecisos | Aplicar reescritas de clareza. Não são seis erros de concordância. |
| Refinamento | E1-07–11; siglas, decimais, uniformização autoral; coortes; índice do lote | Padronizar sem modificar transcrições experimentais. |

## Bloco final de correções prontas — Buscar → Substituir

Os blocos por achado acima são aplicáveis individualmente. Não executar substituição global de expressões genéricas, como “Proceedings” ou “Conexão Escola”. Em caso de sobreposição, E4-02 prevalece sobre E1-09; para SEDUC, alinhar a chamada a [2024] somente se adotar a referência inferida proposta no Eixo3.

Abaixo estão as sete trocas estruturais completas. Foram extraídas dos arquivos atuais; mudam somente a posição da caption/label, preservando PDF, dimensões e fonte. **São propostas, não alterações aplicadas ou recompiladas nesta auditoria.**



### texto/01_introducao.tex:17

Buscar:
```latex
\begin{figure}[htbp]\centering
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/01_Problema_de_pesquisa.pdf}
\caption{Dilema de calibração entre proteção e atendimento educativo}\label{fig:dilema}
\fonte{Elaboração própria a partir do problema de pesquisa.}
\end{figure}
```

Substituir:
```latex
\begin{figure}[htbp]\centering
\caption{Dilema de calibração entre proteção e atendimento educativo}\label{fig:dilema}
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/01_Problema_de_pesquisa.pdf}
\fonte{Elaboração própria a partir do problema de pesquisa.}
\end{figure}
```

### texto/02_referencial.tex:23

Buscar:
```latex
\begin{figure}[htbp]\centering
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/02_Analise_contextual.pdf}
\caption{Análise contextual da intenção e do tratamento da solicitação}\label{fig:contexto}
\fonte{Elaboração própria com base nos descritores de Brasil (2025) e na regra da PoC.}
\end{figure}
```

Substituir:
```latex
\begin{figure}[htbp]\centering
\caption{Análise contextual da intenção e do tratamento da solicitação}\label{fig:contexto}
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/02_Analise_contextual.pdf}
\fonte{Elaboração própria com base nos descritores de Brasil (2025) e na regra da PoC.}
\end{figure}
```

### texto/03_metodologia.tex:32

Buscar:
```latex
\begin{figure}[htbp]\centering
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/06_Preparacao_e_consulta.pdf}
\caption{Preparação do índice e consulta ao acervo do chat selecionado}\label{fig:acervo}
\fonte{Elaboração própria a partir do manifesto do acervo e da configuração de recuperação.}
\end{figure}
```

Substituir:
```latex
\begin{figure}[htbp]\centering
\caption{Preparação do índice e consulta ao acervo do chat selecionado}\label{fig:acervo}
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/06_Preparacao_e_consulta.pdf}
\fonte{Elaboração própria a partir do manifesto do acervo e da configuração de recuperação.}
\end{figure}
```

### texto/03_metodologia.tex:64

Buscar:
```latex
\begin{figure}[htbp]\centering
\input{texto/figura_protocolo.tex}
\caption{Separação entre histórico, desenvolvimento executado e avaliação final planejada}\label{fig:protocolo}
\fonte{Elaboração própria; a avaliação final depende de ratificação e congelamento.}
\end{figure}
```

Substituir:
```latex
\begin{figure}[htbp]\centering
\caption{Separação entre histórico, desenvolvimento executado e avaliação final planejada}\label{fig:protocolo}
\input{texto/figura_protocolo.tex}
\fonte{Elaboração própria; a avaliação final depende de ratificação e congelamento.}
\end{figure}
```

### texto/04_artefato.tex:9

Buscar:
```latex
\begin{figure}[htbp]\centering
\input{texto/figura_arquitetura.tex}
\caption{Arquitetura do GuardKids e rotas de processamento e registro}\label{fig:arquitetura}
\fonte{Elaboração própria a partir da implementação do protótipo.}
\end{figure}
```

Substituir:
```latex
\begin{figure}[htbp]\centering
\caption{Arquitetura do GuardKids e rotas de processamento e registro}\label{fig:arquitetura}
\input{texto/figura_arquitetura.tex}
\fonte{Elaboração própria a partir da implementação do protótipo.}
\end{figure}
```

### texto/04_artefato.tex:21

Buscar:
```latex
\begin{figure}[htbp]\centering
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/05_Processamento_da_pergunta.pdf}
\caption{Percurso de uma pergunta e pontos de encerramento no GuardKids}\label{fig:percurso}
\fonte{Elaboração própria a partir do fluxo da PoC.}
\end{figure}
```

Substituir:
```latex
\begin{figure}[htbp]\centering
\caption{Percurso de uma pergunta e pontos de encerramento no GuardKids}\label{fig:percurso}
\includegraphics[width=\textwidth,height=0.82\textheight,keepaspectratio]{diagramas/pdf/05_Processamento_da_pergunta.pdf}
\fonte{Elaboração própria a partir do fluxo da PoC.}
\end{figure}
```

### texto/04_artefato.tex:49

Buscar:
```latex
\begin{figure}[htbp]\centering
\input{texto/figura_decisao.tex}
\caption{Precedência das decisões de entrada e saída}\label{fig:decisao}
\fonte{Elaboração própria; regras implementadas na função \texttt{decision}.}
\end{figure}
```

Substituir:
```latex
\begin{figure}[htbp]\centering
\caption{Precedência das decisões de entrada e saída}\label{fig:decisao}
\input{texto/figura_decisao.tex}
\fonte{Elaboração própria; regras implementadas na função \texttt{decision}.}
\end{figure}
```

## Verificação da entrega

42 arquivos existentes conferidos por SHA-256: nenhum alterado por esta auditoria. O relatório e o resumo de cálculos são os únicos novos artefatos desta entrega. O PDF e o ZIP do TCC permanecem preservados. Não foi executada inferência nem preenchido julgamento humano.
