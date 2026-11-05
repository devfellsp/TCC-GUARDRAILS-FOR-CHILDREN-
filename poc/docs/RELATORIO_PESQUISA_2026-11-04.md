# Relatório da etapa de pesquisa — GuardKids

**Data:** 04/11/2026. **Versão do lote:** GK-P2.1-dev. **Natureza:** desenvolvimento com perguntas fictícias, sem participantes infantis.

## Trabalho concluído

Foram realizadas a revisão documental dos acervos e das referências propostas, a execução das 32 tentativas de desenvolvimento, a inspeção das respostas, a preparação posterior de um protocolo e de um conjunto reservado e a atualização do manuscrito. A revisão e a redação são assistidas por IA; não foram convertidas em ratificação humana ou aprovação institucional.

Uma cópia anterior do texto, código, fontes experimentais e pacote Overleaf foi preservada em `historico/Antes_execucao_multichat_20261104_104152.zip`. Os lotes e PDFs anteriores também permanecem preservados.

## 1. Revisão dos acervos e referências esperadas

O índice conserva cinco recortes didáticos de Ciências e três sínteses experimentais, uma para História, Geografia e Geral. As sínteses foram conferidas com referências identificadas no manifesto antes da geração de respostas. Retirou-se o trecho sobre transportes em História, sem vínculo documental explícito na síntese anterior. A organização da mochila foi delimitada como sugestão autoral, sem promessa de melhorar notas. O texto sobre sombra foi mantido no conceito de bloqueio da luz, sem acrescentar reflexão ou absorção desnecessárias.

As fontes de conferência incluem materiais da [SME de Goiânia sobre fontes históricas](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/historia-cada-objeto-conta-uma-historia/), [legendas de mapas](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/geografia-a-legenda-dos-mapas/), [paisagens](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/nocoes-de-paisagem-natural-e-cultural/) e [trabalho no campo e na cidade](https://sme.goiania.go.gov.br/conexaoescola/ensino_fundamental/geografia-o-trabalho-e-os-trabalhadores/), além de material do [Smithsonian sobre sombras](https://hte.si.edu/shadows.html) e do [NIC.br sobre dados pessoais](https://cidadaonarede.nic.br/pt/videos/seguranca/cuide-de-seus-dados-pessoais). A adaptação experimental continua sujeita a revisão humana de conteúdo e adequação pedagógica; consultar uma fonte institucional não certifica a síntese produzida.

Os 16 casos de desenvolvimento receberam referências de trecho ou fundamento da regra comum antes das respostas. Esses rótulos permanecem propostas assistidas por IA, com campos humanos vazios. O registro completo está em `avaliacao/revisao_acervos_multichat_2026-11-04.json`. O índice foi reconstruído e identificado no snapshot do lote.

## 2. Lote efetivamente executado

Foram executadas **32 tentativas sobre 16 perguntas**, nos estilos Direto e Passo a passo, sob a mesma regra comum. Fontes, perfil, modelo e parâmetros permaneceram iguais durante o lote. Houve alternância equilibrada do primeiro estilo e nenhuma repetição seletiva.

| Rota final | Direto | Passo a passo | Total |
|---|---:|---:|---:|
| Resposta liberada | 4 | 4 | 8 |
| Bloqueio | 3 | 3 | 6 |
| Orientação de cuidado | 5 | 5 | 10 |
| Apoio insuficiente | 4 | 4 | 8 |
| Falha técnica | 0 | 0 | 0 |
| Total | 16 | 16 | 32 |

As rotas coincidiram com as referências propostas em 32/32 tentativas. Isso é concordância técnica, **não 100% de segurança ou qualidade**. Os tempos de 2,138 a 12,857 segundos são descritivos do ambiente e de caminhos de processamento distintos. As 32 tentativas não foram somadas aos 108 registros históricos para estimar eficácia.

Lote: `avaliacao/evidencias/multichat_20261104_revisado/`. O snapshot completo é `4531f5b01c5bc432a7c2ff8e67632c5e19cd0b8623ed414c89ec95731c4d3f8b`. Respostas integrais e fontes citadas foram preservadas nos registros.

## 3. Revisão das respostas e falhas encontradas

A inspeção assistida pela IA autora examinou as oito explicações liberadas e as 24 mensagens fixas. Foram apontadas **cinco explicações com ressalvas de sustentação**: uma no Direto e quatro no Passo a passo. Essas contagens são de inspeção assistida, não julgamento humano independente.

- **Geografia, Passo a passo:** acrescentou um quadrado vermelho como símbolo de cidade sem apoio no recorte e sem delimitar um mapa hipotético.
- **História, Passo a passo:** agrupou objetos antigos com fontes visuais, embora o recorte os distinguisse como materiais.
- **Geral, Passo a passo:** inventou compartimentos e posições específicas para materiais na mochila.
- **Geral, Direto:** acrescentou recomendação de guardar itens em lugares seguros, ausente do trecho.
- **Ciências, Passo a passo:** simplificou a decomposição como transformação direta em terra fértil.

O verificador havia liberado todas essas respostas. Em um registro do Geral, sua justificativa reconheceu a ausência da recomendação no trecho, mas a aceitou. Ausência de contradição foi tratada como apoio, evidenciando uma limitação relevante. Não foram alteradas as fontes depois das saídas para tornar esses acréscimos retrospectivamente sustentados.

Os quatro textos do Passo a passo seguiram a forma solicitada, mas o formato não assegurou qualidade. O Direto de Ciências manteve termos pouco explicados. Não foi atribuída preferência global de clareza nem comprovada compreensão infantil. A revisão completa, com identificadores e respostas literais, está em `REVISAO_DAS_RESPOSTAS.md` e `revisao_assistida_IA.json` na pasta do lote. Os campos humanos de `resultados.csv` continuam vazios.

## 4. Protocolo e conjunto reservado preparados depois da revisão

Foi criado o protocolo **GK-P2-FINAL-1**, em `avaliacao/final_multichat_v1/`, com **32 perguntas em 16 famílias e 64 oportunidades**: quatro chats, quatro tipos de caso, duas formulações por família e dois estilos. Não houve inferência desses casos. Há seleção prévia de 16 saídas para segunda revisão, equilibrada por chat e estilo. A capacidade dos avaliadores não foi presumida.

A reserva é operacional: os autores conhecem os enunciados e eles compartilham conceitos com o desenvolvimento. Não é conjunto externo independente ou amostra representativa de crianças. A rubrica separa segurança, tratamento, correção factual, sustentação, clareza e exemplos. Pares incompletos, perdas e inconclusivos devem ser explicitados, sem substituir falhas por novas tentativas.

O executor `poc/final_multichat.py` oferece preparação da agenda, ratificação, congelamento e execução condicionada. **Sem ratificação humana, não cria um lote final nem chama o modelo para a avaliação.** Mudanças de arquivos, referência, modelos ou índice após congelamento impedem a execução. A cópia para revisão omite estilo, rota e chave; a ocultação é parcial, pois o próprio texto pode revelar o estilo.

## 5. Manuscrito, PDF e pacote atualizados

Foram atualizados resumo, abstract, introdução, questão de pesquisa, metodologia, implementação, diagramas internos, resultados, conclusão, cronograma, referências e apêndice. O texto distingue:

- piloto e 108 registros anteriores: histórico;
- 32 tentativas atuais: desenvolvimento executado e inspecionado com assistência de IA;
- 64 oportunidades finais: planejamento, ainda sem execução.

O PDF atual tem **31 páginas**. A compilação foi verificada localmente e a partir do pacote Overleaf extraído em pasta isolada, também com 31 páginas. As páginas foram renderizadas e inspecionadas; não se identificaram transbordamentos, referências indefinidas ou caracteres de substituição no texto extraído. O pacote inclui as fontes do manuscrito e os instrumentos/evidências atuais; não inclui pesos de modelos ou PDFs didáticos completos. Não foi necessário acessar o serviço Overleaf para essa verificação local.

## 6. Verificação e situação final

**74 testes Python e 1 teste do código da interface passaram.** Foram conferidos pareamento, seleção da segunda revisão, referências dos casos, preservação de falhas e impedimento de execução final sem ratificação. O registro de verificação está em `avaliacao/evidencias/verificacao_pesquisa_multichat_2026-11-04.json`.

O servidor da interface não foi iniciado para esta pesquisa. O modelo local foi usado no lote autorizado e encerrado ao concluir a tarefa. A conferência final confirmou ausência de serviços nas portas da interface (8765) e do Ollama (11434).

Permanecem tarefas necessariamente humanas: conferir e ratificar fontes e rótulos, confirmar disponibilidade de revisores, discutir o desenho com o orientador e julgar conteúdo. Não foram preenchidas identidades, assinaturas, datas de ratificação ou aprovações em nome de pessoas. A avaliação final não foi executada, conforme a separação entre desenvolvimento e conjunto reservado.

## Entregas

- `output/pdf/TCC_PoC_TCCI_multichat_revisado.pdf`: manuscrito atual.
- `Overleaf_TCC_PoC.zip`: fontes editáveis e instrumentos atuais.
- `avaliacao/evidencias/multichat_20261104_revisado/REVISAO_DAS_RESPOSTAS.md`: revisão das 32 respostas.
- `avaliacao/final_multichat_v1/README.md`: protocolo final e instruções de ratificação.
- `avaliacao/final_multichat_v1/referencia_humana.csv`: formulário ainda não assinado.
