# Parecer acadêmico do TCC GuardKids

Data: 03/11/2026. Objeto: versão local atual de `main.tex`, após as correções técnicas. Esta análise não modifica o texto do TCC nem o programa.

## Avaliação geral

O trabalho apresenta problema delimitável, protótipo executável, políticas configuráveis e registros que permitem examinar decisões. Seu núcleo mais defensável é o desenvolvimento de uma prova de conceito e de um protocolo para analisar a exceção contextual de predação educativa.

O principal ponto pendente é a distância entre esse estágio e a promessa de avaliar o equilíbrio entre proteção e atendimento educativo. Os resultados atuais demonstram funcionamento e calibração em casos de desenvolvimento; a avaliação independente de conteúdo e qualidade ainda está pendente. A correção de software não encerra essa etapa científica.

Para projeto ou qualificação, essas pendências podem integrar o plano de execução, desde que explicitadas. Para uma monografia final que mantenha o objetivo de avaliação comparativa, será necessário produzir as evidências correspondentes ou reformular o objetivo com o orientador. Não foi atribuído conceito de aprovação nem presumido o regulamento específico da disciplina.

## 1. Correções prioritárias de coerência

### 1.1 Resumo e abstract ainda excedem as evidências

**Onde:** `main.tex`, linhas 194 e 202; contraste com as linhas 783, 789 e 825.

Os dois resumos ainda dizem que o ajuste preserva proteção e elimina recusas indevidas. O capítulo de resultados e a conclusão reconhecem que concordância de rotas não permite concluir eficácia de conteúdo, e que os julgamentos humanos estão pendentes.

**Melhoria:** descrever a entrega como desenvolvimento, validação funcional e calibração preliminar. Informar que houve diferença de rota no caso de predação e que a avaliação independente permanece pendente. Atualizar português e inglês juntos. Não basta acrescentar uma ressalva apenas à conclusão.

### 1.2 Título, público e unidade avaliada precisam ter o mesmo alcance

**Onde:** linhas 99, 288, 299 e 428.

O título e a pergunta de pesquisa mencionam crianças de sete a onze anos, mas o estudo opera com um perfil fictício de nove anos, um componente curricular e nenhum participante infantil. A delimitação está explicada na metodologia, o que é positivo; ainda assim, a abertura pode sugerir alcance maior que o avaliado.

**Melhoria:** decidir entre destacar no título o cenário de Ciências do quarto ano ou manter o público destinatário amplo e tornar a delimitação muito visível no resumo e nas conclusões. Diferenciar destinatário pretendido, perfil de teste e população efetivamente observada. Não é necessário incluir crianças para resolver isso; basta ajustar o alcance das afirmações.

### 1.3 O documento mistura projeto, estudo preliminar e monografia final

**Onde:** preâmbulo na linha 107; objetivos nas linhas 299–306; avaliação futura nas linhas 829–834; cronograma nas linhas 852–869.

O preâmbulo diz projeto, o texto se apresenta como monografia, parte dos procedimentos aparece no futuro e o capítulo se chama Resultados. O objetivo de avaliação comparativa ainda não está cumprido na versão atual. O cronograma prevê para meses futuros atividades que já ocorreram parcialmente no piloto.

**Melhoria:** declarar a etapa acadêmica do documento e separar realizado, em andamento e planejado. Distinguir o piloto já executado da avaliação final prevista. No encerramento, apresentar uma matriz de objetivos com entrega, evidência e situação, sem afirmar cumprimento integral de uma avaliação ainda não realizada.

## 2. Fortalecimento do desenho experimental

### 2.1 A comparação pode demonstrar apenas o efeito que foi programado

**Onde:** função de decisão nas linhas 618–625 e políticas nas linhas 723–726.

As configurações diferem somente em permitir predação educativa. Para uma classificação fixa com `needs_protection=false` e `educational_predation=true`, a troca de decisão decorre da própria definição da regra. Mostrar esse caso comprova que o parâmetro funciona, mas não demonstra que o classificador separa contextos difíceis de forma confiável.

**Melhoria:** explicitar que a referência é uma ablação conservadora. Formular expectativas verificáveis: redução de recusas em perguntas educativas sobre predação e observação de possíveis respostas inadequadas em solicitações de risco próximas desse contexto. Usar paráfrases, ambiguidades e pedidos mistos novos. A contribuição científica passa a ser a análise dos acertos e erros da fronteira contextual, não somente a alteração do booleano.

Não é obrigatório acrescentar vários modelos ou construir outro sistema. Um experimento delimitado, com casos difíceis e avaliação bem documentada, responde melhor à pergunta atual.

### 2.2 Falta fechar o protocolo de amostragem e execução

**Onde:** linhas 495–524 e 583.

Os grupos estão definidos, mas faltam tamanho final da amostra, distribuição por categoria, critérios de seleção, adaptação linguística, número de repetições, ordem das condições e tratamento operacional dos pares com erro. As 22 execuções históricas representam 11 perguntas, não 22 perguntas independentes.

**Melhoria:** criar uma tabela de protocolo com esses campos, justificando cada decisão por escopo e recursos. Documentar origem e adaptação de cada caso, separar desenvolvimento e avaliação e identificar famílias de paráfrases. Definir se a unidade de análise é pergunta, execução ou família de casos. Se houver repetições, evitar apresentá-las como perguntas independentes.

O tamanho não precisa ser escolhido por uma regra arbitrária de cem perguntas: deve resultar da cobertura desejada e ser compatível com a avaliação humana disponível.

### 2.3 Ausência de apoio no corpus não deve ser definida pelo resultado da busca

**Onde:** linha 516.

O grupo de perguntas sem apoio é associado a similaridade abaixo do limiar. Essa associação torna a referência dependente do comportamento do próprio recuperador. Uma pergunta pode ter similaridade alta e não ter resposta nas fontes; outra pode ter apoio real e obter similaridade baixa.

**Melhoria:** classificar apoio ou ausência de apoio pela leitura do corpus antes de executar o sistema. Incluir perguntas próximas do tema cuja resposta específica não esteja nos trechos, além de perguntas obviamente distantes. Manter separados: estar no tema, existir apoio no corpus e o recuperador encontrar esse apoio.

### 2.4 Justificar parâmetros com calibração documentada

**Onde:** linhas 603, 605 e 612.

Limiar 0,45, três trechos, blocos de 850 caracteres, contexto de 4096 tokens e limite de 120 palavras são apresentados como configurações, mas a escolha ainda carece de uma justificativa empírica ou operacional suficiente.

**Melhoria:** registrar quais casos de desenvolvimento orientaram cada escolha, quais alternativas foram examinadas e por que a versão foi adotada. Uma comparação pequena de limiares pode ser suficiente; não é necessário otimizar todo parâmetro. Congelar as decisões antes de observar a avaliação final e considerar o orçamento de contexto com pergunta, instruções, fontes e resposta.

## 3. Julgamento e indicadores

### 3.1 Tornar a rubrica aplicável por outra pessoa

**Onde:** linhas 554–576.

Integral, parcial e ausente são níveis compreensíveis, mas ainda deixam margem para interpretações diferentes. Correção factual, fidelidade à fonte e clareza precisam ser examinadas como propriedades distintas.

**Melhoria:** fornecer exemplos anotados de cada nível, critérios de desempate e regras para afirmações verdadeiras sem apoio. Registrar avaliador, data e justificativa. Quando viável, solicitar segunda avaliação de parte da amostra, ocultando a configuração da resposta e registrando discordâncias. Se isso não for viável, descrever a revisão por um único avaliador e seu limite, sem inventar independência.

Avaliar clareza textual para um perfil não equivale a demonstrar compreensão por crianças. A ausência de participantes infantis é uma delimitação legítima e deve continuar explícita.

### 3.2 Medir segurança e atendimento educativo separadamente

**Onde:** linhas 532–550 e 556.

A taxa global de inadequação depende da mistura de grupos: acrescentar muitas perguntas benignas pode reduzir a porcentagem global sem melhorar o tratamento de riscos. Além disso, uma configuração pode parecer segura simplesmente por não responder.

**Melhoria:** apresentar contagens e taxas por grupo e categoria, além do agregado; manter numeradores e denominadores; mostrar diferenças pareadas entre políticas. Acrescentar a proporção de perguntas legítimas que efetivamente recebem resposta segura, correta e sustentada. Registrar separadamente bloqueio indevido, redirecionamento indevido, insuficiência correta e erro técnico.

O texto já reconhece perdas e inconclusivos, mas precisa definir como isso será aplicado aos pares na análise. Um bloqueio correto de saída pode ser proteção bem-sucedida e, ao mesmo tempo, falta de atendimento educativo; as duas informações devem aparecer.

## 4. Políticas, corpus e finalidade educativa

### 4.1 Refinar tratamentos esperados e mapear todas as categorias

**Onde:** linhas 453–465 e 518.

A linha sobre ofensas inclui solicitação de explicação de termos ofensivos como motivo de bloqueio. Isso pode abranger uma criança buscando compreender ou relatar uma situação de bullying. A categoria substâncias admite bloqueio ou orientação, mas não explicita a regra que decide entre esses tratamentos. Injeção de prompt aparece nos testes e no classificador, mas não tem linha própria no quadro de políticas.

**Melhoria:** separar intenção de causar dano, busca de ajuda, relato de experiência e explicação educativa. Incluir pares mínimos de exemplos e respectivas justificativas. Criar correspondência entre categorias da literatura, descritores usados como referência, rótulos do programa e julgamento esperado. Não inferir conformidade legal ou classificação oficial apenas por essa correspondência.

### 4.2 Justificar curricularmente o recorte

**Onde:** linhas 428, 475 e 692–717.

O cenário de Ciências está delimitado, mas o vínculo com objetivos de aprendizagem pode ficar mais explícito. Há habilidades curriculares diretamente relacionadas a cadeias alimentares e decomposição: EF04CI04 e EF04CI06 são apresentadas, por exemplo, no [referencial curricular oficial do Paraná](https://www.referencialcurriculardoparana.pr.gov.br/Ciencias-4o-Ano).

**Melhoria:** mapear objetivos de aprendizagem a trechos do corpus, perguntas e critérios de qualidade; conferir a redação aplicável na BNCC e no referencial adotado pelo curso/escola. Explicar por que cinco passagens bastam para o domínio efetivamente avaliado. Ampliar o corpus somente se isso for necessário ao escopo declarado, com revisão do conteúdo; mais páginas não asseguram melhor avaliação.

### 4.3 A tabela do acervo precisa descrever o índice real

**Onde:** linhas 709–715, comparadas com os textos dos cinco chunks do índice local ativo.

Há descrições mais amplas do que os recortes efetivamente indexados: fitoplâncton na linha 709; lista de proteínas, lipídios, vitaminas e sais minerais na linha 711; algas e certas bactérias na linha 713; herbívoros/carnívoros/onívoros na descrição do recorte da linha 715. Esses termos não constam dos respectivos textos recuperáveis do índice conferido. Isso não significa que os conceitos sejam falsos nem que estejam ausentes de toda a obra: o problema é atribuí-los àquele recorte específico.

**Melhoria:** conferir cada resumo contra o chunk real, separando página completa, trecho selecionado e conhecimentos externos. Gerar essa tabela a partir de metadados conferidos pode reduzir novas divergências. A correção científica das fontes também merece revisão especializada; fidelidade ao material não basta para provar correção factual.

## 5. Texto, fundamentação e apresentação

### 5.1 Explicitar a lacuna e a contribuição

**Onde:** resumo na linha 194, introdução e revisão nas linhas 279–415.

A alegação de escassez de estudos em português brasileiro não vem acompanhada de um procedimento de busca. O referencial descreve bem as referências selecionadas, mas precisa explicitar melhor o que cada trabalho deixa em aberto e qual contribuição concreta o GuardKids pretende oferecer.

**Melhoria:** apresentar uma revisão narrativa estruturada, com bases consultadas, termos, período e critérios de seleção. Isso não exige declarar uma revisão sistemática. Acrescentar comparação entre idioma, público, tipo de proteção, avaliação e limites dos trabalhos. Posicionar a contribuição como operacionalização e avaliação contextual em cenário delimitado, sem reivindicar invenção de RAG ou de verificadores de entrada e saída.

A referência de NeMo tem publicação formal e DOI na [ACL Anthology](https://aclanthology.org/2023.emnlp-demo.40/); as páginas 431–445 informadas no TCC foram confirmadas. Na revisão bibliográfica, distinguir ferramenta efetivamente usada de inspiração arquitetural: citar NeMo e Llama Guard não significa que esses sistemas tenham sido implementados no protótipo.

### 5.2 Unificar a descrição da versão avaliada

**Onde:** linhas 493, 604, 609–615, algoritmo das linhas 652–687 e revisão posterior nas linhas 811–817.

A descrição principal ainda apresenta caminhos de índice legados, campos de âncora diferentes dos usados no manifesto e registro integral como comportamento geral. O algoritmo não inclui a verificação adicional de sustentação; ela só é explicada perto do fim. A discussão de latência fala em três chamadas ao LLM, correspondente ao piloto, enquanto a versão atual pode realizar quatro.

**Melhoria:** escolher e identificar a versão objeto da avaliação. Apresentar sua arquitetura e pseudocódigo completos em um único lugar. Colocar o histórico de correções e os dados antigos em subseções claramente identificadas ou apêndices. Incluir uma tabela com versão, alterações, prompts, dados e evidência disponível. Não utilizar tempos de uma versão para caracterizar outra.

### 5.3 Reduzir afirmações absolutas e aumentar discussão crítica

**Onde:** linhas 271, 311 e 379, entre outras.

Expressões como assegurar cumprimento ou garantir rastreabilidade precisam ser qualificadas. Há também descrição extensa de implementação e menos discussão de falhas, alternativas e limites do que seria desejável para responder à pergunta científica.

**Melhoria:** distinguir intenção do mecanismo, garantia determinística efetivamente implementada e resultado empírico observado. Mover detalhes de endpoints, estrutura de pastas e comandos para apêndices quando não forem necessários ao argumento. Reservar a discussão principal para falsos bloqueios, conteúdo inadequado, falta de apoio, erros técnicos e custos da proteção.

### 5.4 Completar figuras, elementos formais e cronograma

**Onde:** lista de ilustrações, preâmbulo na linha 107, folha de aprovação nas linhas 156–157 e palavras-chave nas linhas 196 e 206.

Há sete diagramas no projeto, mas o corpo do documento não inclui figuras de arquitetura ou protocolo; as inclusões gráficas do LaTeX correspondem aos logotipos. A lista de ilustrações fica sem essas figuras. A folha de aprovação mantém nomes genéricos, e a denominação institucional varia entre Fundação e Universidade Estadual. A expressão portuguesa está como Palavras-chaves.

**Melhoria:** inserir apenas os diagramas que sustentam o argumento — arquitetura, decisão e protocolo são candidatos —, com legenda, fonte e chamada no texto; adequar a lista ao conteúdo. Conferir modelo e denominação institucional com o manual vigente, preencher nomes de banca quando definidos e revisar Palavras-chave/Keywords, referências e datas de acesso. Não foi presumida conformidade integral com ABNT ou com o manual institucional apenas pela compilação do PDF.

## Sequência recomendada

1. Alinhar resumo, abstract, título, objetivo e etapa acadêmica.
2. Fixar pergunta operacional, comparação, amostra, referência humana, protocolo e indicadores.
3. Conferir quadro de políticas, descrição dos recortes e vínculo curricular.
4. Consolidar a versão a ser avaliada e atualizar o pseudocódigo e as figuras.
5. Executar avaliação independente, documentar julgamentos e discutir resultados favoráveis e desfavoráveis.
6. Revisar conclusão, elementos formais e apresentação com base nas evidências finais.

O foco recomendado é obter uma avaliação pequena, coerente e rastreável. Acrescentar funcionalidades, modelos, áudio, imagens ou participação de crianças antes de fechar o experimento atual tende a ampliar o escopo sem resolver a lacuna central.
