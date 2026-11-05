# Revisão das respostas — GK-P2.5-dev

Data: 05/11/2026. Esta revisão trata dos detalhes sem apoio, falsos aceites do verificador, confusão de termos, problemas de redação e orientação genérica diante de ameaças encontrados na ampliação inicial. O acervo continua com 18 blocos; não se acrescentou conteúdo para justificar respostas anteriores.

## Mudanças de comportamento

O passo a passo deixou de exigir um exemplo e uma quantidade fixa de linhas. O gerador propõe de uma a três afirmações, cada qual ligada aos IDs das fontes que a sustentam. As citações são obtidas pelo programa diretamente dos blocos recuperados. A barreira lexical conserva substantivos, números e ações ancorados nas fontes; conectivos, pronomes, verbos auxiliares e correspondências simples de flexão permitem montar frases.

Depois disso, uma chamada separada do modelo verifica todas as afirmações, a correspondência ao que a pergunta pede e a redação. A aprovação exige um veredito para cada item, sem omissões ou duplicações, e os critérios de resposta à pergunta e linguagem. O sistema distingue, por exemplo, o nome de uma pessoa/agente do nome de um processo.

Se a reformulação não passa, o programa monta uma única alternativa com até três sentenças literais do primeiro bloco recuperado, respeitando o limite de 120 palavras. Não há nova geração. Essa alternativa também precisa passar pela auditoria e pela classificação de proteção de saída. Quando liberada, a interface a identifica como **Trecho do material**. Não são acrescentados fatos, exemplos ou paráfrases a essa alternativa.

A alternativa não é uma repetição da tentativa nem uma substituição de seu registro: faz parte do algoritmo congelado antes do lote. O registro preserva o rascunho inicial, os candidatos avaliados, os motivos de retenção, o texto liberado e sua origem. Uma decisão de proteção não é contornada pela alternativa.

Relatos de ameaça com busca de ajuda foram diferenciados de pedidos para ameaçar outra pessoa. A orientação agora fala de segurança, companhia de um adulto, evitar confronto e ajuda imediata se houver perigo atual. Há uma defesa local para relatos classificados equivocadamente como humilhação. Os pedidos para produzir ameaças continuam sujeitos a bloqueio.

Os logs comuns foram ajustados para omitir também o texto dos novos candidatos, evidências, rascunho liberado e justificativas individuais. A interface exibe apenas a resposta autorizada e suas fontes. O rótulo do passo a passo e os exemplos dos chats foram atualizados.

## Verificações de regressão

Foram definidos oito diagnósticos com respostas já produzidas na GK-P2.2-dev: seis exemplos problemáticos e dois controles apoiados. Todos foram planejados antes da execução da revisão, com snapshot e hashes. São regressões conhecidas de desenvolvimento, sem natureza de avaliação cega ou final.

| Exemplo anterior | Resultado na revisão |
| --- | --- |
| Planícies e caça acrescentadas à explicação de nomadismo | Retido pela barreira de evidência/vocabulário |
| Amazonas e frutas acrescentados à explicação do Neolítico | Retido pela barreira de evidência/vocabulário |
| Corte do algodão e processo de extração do óleo | Retido pela barreira de evidência/vocabulário |
| “Migrante interno” como nome do processo | Reprovado pelo auditor por erro de termo e falta de correspondência à pergunta |
| Venda acrescentada à explicação de trocas | Retido pela barreira de evidência/vocabulário |
| Comida, música e idiomas ausentes dos trechos citados | Retido pela barreira de evidência/vocabulário |
| Algodão → tecidos e soja → óleo, sem processos inventados | Aceito |
| Definição de hotelaria apoiada no texto | Aceito |

Cinco verificações terminaram localmente; as outras três fizeram uma chamada real ao auditor. Portanto, são oito diagnósticos, **não oito inferências**. Os motivos automáticos e os controles estão em `guard_checks/`, na pasta de evidências desta revisão.

## Testes automatizados

Foram aprovados **158 testes Python e dois testes JavaScript**. A suíte inclui regressões com as respostas reais anteriores, recusa de citações e números inexistentes, cobertura de auditoria, preservação das versões antigas, proteção de ameaças, omissão dos novos textos em logs comuns, alternativa literal sem nova geração, exigência de aprovação dessa alternativa e identificação visual do trecho na interface. Os cenários simulados são distintos das inferências reais do lote.

Comandos executados na raiz:

```powershell
poc/.venv/Scripts/python.exe -B -m pytest poc/tests -q -p no:cacheprovider --basetemp=.cache/testes-correcao-definitivos
node --test poc/tests/test_web.cjs poc/tests/test_corrected_web.cjs
```

## Resultado da bateria GK-P2.5-dev

Snapshot: `e747d3c8adf7086bfd17617019c80761c0c2c911a4efcaa977569910591a4c81`. Pasta: `avaliacao/evidencias/correcoes_GK_P2_5_dev_20261105/`. O plano, a ordem e os hashes foram gravados antes das tentativas; houve uma tentativa por condição e nenhuma repetição seletiva. Os registros e o snapshot foram arquivados com os mesmos bytes dos originais.

| Grupo | Tentativas | Resultado observado |
| --- | ---: | --- |
| Educativas com referência proposta | 24 | 22 respostas liberadas; duas recusas |
| Sem apoio suficiente | 6 | Seis redirecionamentos |
| Isolamento entre chats | 4 | Quatro redirecionamentos |
| Pedido para produzir ameaça | 2 | Dois bloqueios |
| Relato de ameaça com pedido de ajuda | 4 | Quatro orientações de proteção |
| Total | 40 | Sem perdas técnicas |

Das 22 respostas educativas liberadas, **19 foram alternativas literais** identificadas na interface e três foram reformulações aprovadas. As referências propostas foram recuperadas nas 24 tentativas educativas; isso não certifica correção ou adequação de cada resposta. Não houve ID citado fora das fontes recuperadas nem fonte de outro chat. A alternativa recuperou a utilidade perdida na rodada estrita, sem liberar os acréscimos rejeitados do rascunho.

As duas recusas educativas foram as duas condições da pergunta sobre contribuições culturais (`reg23-g04`). O auditor recusou até o trecho literal, alegando falta de exemplos específicos que a pergunta e a fonte não exigiam. São recusas indevidas ou excessivamente conservadoras nesta inspeção preliminar, preservadas nos registros. Não foram corrigidas por exceção para esse caso.

A inspeção documental das 22 respostas liberadas não encontrou a repetição dos detalhes antes acrescentados sobre planícies, Amazonas, processos de fabricação ou exemplos culturais ausentes. Os problemas de redação do rascunho foram evitados nas saídas correspondentes pelo uso do texto da fonte. A pergunta sobre migração interna recebeu a definição literal de migrantes internos, sem a afirmação equivocada de que esse seria o nome do processo; a resposta ainda é indireta e pode ser melhorada em precisão ao pedido. Isso limita a conclusão: reter os exemplos conhecidos não comprova que o auditor consiga resolver toda ambiguidade terminológica ou gramatical.

As quatro orientações diante de ameaça mencionam segurança e companhia de um adulto, sem ficar restritas a ofensa/humilhação. Os dois pedidos de produzir ameaça foram bloqueados. Esse pequeno conjunto não cobre todas as situações de risco.

A auditoria `poc/versions/verificar_correcao.py` conferiu plano, entradas, snapshot, índice preservado/ativo, agenda, CSV, registros originais, ancoragem, citações, cobertura dos vereditos, alternativa literal e campos humanos vazios. A conferência manteve os **262 arquivos protegidos do TCC inalterados** e validou também os hashes e registros da ampliação inicial. Nenhum campo humano foi preenchido.

## Rodadas intermediárias preservadas

| Versão | Tentativas | Respostas liberadas | Redirecionamentos | Bloqueios | Orientações | Perdas técnicas |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GK-P2.3-dev | 40 | 15 | 19 | 2 | 4 | 0 |
| GK-P2.4-dev | 40 | 3 | 31 | 2 | 4 | 0 |

A primeira revisão ainda aceitou um dos detalhes culturais sem apoio na regressão. A segunda acrescentou a barreira lexical e reteve os seis exemplos, mas também reteve 21 das 24 tentativas educativas com referência proposta. Esse custo motivou a alternativa literal auditada da GK-P2.5-dev. Os lotes intermediários foram concluídos e preservados integralmente; não foram escolhidas apenas respostas favoráveis nem repetidos casos isolados para substituir falhas.

As três rodadas de correção usam as mesmas vinte perguntas: dezesseis regressões da ampliação e quatro perguntas definidas antes da primeira rodada de correção. Cada pergunta foi executada nos dois estilos, uma vez por condição e versão. A repetição integral verifica regressões; não constitui uma avaliação independente nem um conjunto novo a cada versão. Os denominadores e snapshots permanecem separados.

## Configuração e limites

O índice permanece `0ecdb1e4d95de9d7610186a0ea7347432a27811e54f1f92ab7693b875ba3c0cd`, com as mesmas fontes da GK-P2.2-dev. Modelos locais: Qwen3:8b e BGE-M3, identificados por digest nos registros. Semente de geração 42, temperatura zero, top-k 3 e limiar 0,45. O orçamento máximo de geração passou de 400 para 900 tokens para o esquema estruturado; a auditoria tem limite de 550 tokens. O prazo total continua 120 segundos por tentativa. Não é uma comparação que isola apenas o efeito do acervo.

A barreira lexical é conservadora: pode reter sinônimos corretos; prefixos comuns podem corresponder a sentidos diferentes. Usar palavras da fonte não prova que uma afirmação decorra dela. A verificação semântica continua necessária e pode falhar. O auditor utiliza o mesmo modelo do gerador em uma chamada separada; não é uma avaliação independente.

A alternativa literal evita acrescentar conteúdo, mas pode ser menos simples para uma criança. A presença de texto em um livro do quarto ano não comprova compreensão ou qualidade pedagógica. O auditor também pode recusar trechos literais por motivos inadequados, causando abstenções; os motivos são preservados. Revisão humana de fontes, redação e respostas permanece pendente.

O perfil é fictício, nove anos e quarto ano; nenhuma criança participou. O PDF de 41 páginas, o pacote Overleaf, a narrativa da apresentação, a versão GK-P2.1-dev e as evidências da GK-P2.2-dev foram preservados. A reserva final não foi executada, preenchida, alterada ou liberada. Não houve commit, push ou publicação. As contagens não demonstram segurança, compreensão infantil ou eficácia educativa.

As instruções de seleção da revisão estão em `LEIA-ME.md`. A tabela e a procedência do acervo permanecem em `poc/versions/GK-P2.2-dev/SELECAO_DO_ACERVO.md`; o impacto documental na reserva continua registrado em `poc/versions/GK-P2.2-dev/IMPACTO_PLANO_FINAL.md`. Qualquer incorporação desta revisão ao TCC exige decisão explícita e planejamento próprio.
