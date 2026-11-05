# Aplicação da atualização do TCC — GK-P2.6-dev

Data: 05/11/2026. Estado: concluído conforme o plano salvo.

## Escopo aplicado

Manuscrito atualizado para dez chats e 40 blocos; seis volumes de quatro coleções e três sínteses. Resumo, Abstract, introdução, materiais, arquitetura, resultados, conclusão e cronograma alinhados à GK-P2.6-dev. A revisão do referencial teórico foi limitada às ligações com o novo escopo. Quatro novas referências documentais foram incluídas, totalizando 24.

Os resultados foram separados por versão: piloto de 22 execuções, dois lotes históricos com 108 execuções sobre 27 perguntas reutilizadas, 32 tentativas da GK-P2.1-dev e verificações de desenvolvimento da GK-P2.6-dev. As 32 perguntas/64 oportunidades continuam identificadas como proposta anterior; a avaliação da ampliação depende de replanejamento. Nenhum quantitativo final foi inventado.

Cinco diagramas foram editados nos originais Draw.io e sincronizados nos dois arquivos conjuntos: 03, 04, 05, 06 e 07. Os diagramas conceituais 01 e 02 foram preservados. Todos os PDFs alterados foram exportados pelo Draw.io, mantendo os caminhos usados pelo LaTeX. Duas caixas do diagrama de evidências foram ampliadas após a inspeção para acomodar seus rótulos. O cronograma LaTeX foi mantido: oito figuras no total, sendo sete diagramas Draw.io.

## Validação da entrega

- PDF final: 44 páginas, oito figuras, dez tabelas e 24 referências.
- Compilação final: três passagens XeLaTeX a partir de extração limpa do novo Overleaf_TCC_Drawio_rotulos.zip, com main.tex como entrada.
- Listas de figuras e tabelas, sumário e referências resolvidos; sem referências indefinidas ou caixas Overfull na compilação final.
- Todas as páginas renderizadas com Poppler e inspecionadas em pranchas; páginas dos diagramas, acervo, histórico, cronograma e referências também conferidas individualmente. Logo presente nas 44 páginas.
- Pacote ZIP verificado por integridade e comparação byte a byte com os arquivos selecionados do projeto. Não inclui ambientes virtuais, modelos, execuções ativas nem os PDFs integrais dos livros. A compilação do manuscrito é independente desses materiais; a reprodução da PoC exige as dependências e os materiais locais descritos nos manifestos.
- Os 110 arquivos JSON/CSV protegidos de registros, protocolos e índices históricos permanecem idênticos aos hashes capturados antes da edição.
- Utilizados os resultados funcionais já registrados: 25 testes Python, um teste de interface e três consultas reais, com a distinção documentada entre as consultas completas e os ajustes posteriores de recursos. Nenhuma nova inferência foi necessária para esta atualização documental.

## Páginas finais

Numeração impressa do manuscrito; a posição física no PDF é uma página a mais.

| Conteúdo | Página impressa | Página física |
|---|---:|---:|
| Materiais e escopo atual | 19 | 20 |
| Tabela do acervo por dez chats | 20 | 21 |
| Preparação e consulta (Figura 3) | 21 | 22 |
| Arquitetura (Figura 4) | 23 | 24 |
| Pipeline (Figura 5) | 25 | 26 |
| Proteção (Figura 6) | 27 | 28 |
| Evidências por versão (Figura 7) | 29 | 30 |
| Verificações da GK-P2.6-dev | 34–35 | 35–36 |
| Histórico de Ciências, com parágrafo de abertura | 35 | 36 |
| Cronograma (Figura 8) | 40 | 41 |
| Referências | 41–43 | 42–44 |

## Preservação e pendências científicas

Backup anterior à edição: historico/Antes_atualizacao_TCC_GK_P2_6_20261105.zip. Os registros experimentais e protocolos existentes foram preservados. A exclusão de Cronograma.pdf já existente no estado inicial do Git não foi revertida; a figura do cronograma permanece gerada por texto/cronograma.tex.

A revisão humana dos novos recortes, a conferência das condições de reutilização e o replanejamento/congelamento da avaliação final permanecem pendentes e estão declarados no manuscrito. As verificações funcionais não demonstram eficácia pedagógica, segurança geral ou aprendizagem infantil. Não houve commit ou push nesta atualização, pois não foram solicitados para esta etapa.
