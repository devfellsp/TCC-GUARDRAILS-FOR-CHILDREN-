# Revisão prospectiva: balanceamento, ASCS e mensagens de ajuda

Revisão autorizada pelo autor em 04/11/2026, anterior à ratificação, ao congelamento e à execução final.

## Alterações

- Segunda revisão: uma saída por família; em cada chat e grupo, duas de cada estilo. Ordem das 64 tentativas e identificadores das respostas preservados. Regeneradas somente as seleções prospectivas e seus formulários secundário e de conciliação, previamente conferidos como vazios.
- ASCS: escopo de oito oportunidades educativas por estilo, critérios de sucesso e regras dos denominadores conclusivo e por oportunidade documentados no manuscrito, README e protocolo JSON. Recusas indevidas não desaparecem do denominador conclusivo; pendências não viram erros; inconclusivos e perdas permanecem separados de falhas de conteúdo comprovadas. O cálculo automático histórico ainda não implementa o desenho atual.
- Clareza: novo formulário comparacao_clareza.csv com 32 pares e campos humanos vazios. Uso após os pareceres individuais, apenas em pares completos e pertinentes.
- Resultados: documentadas as mensagens de mc-g04 (privacidade sem orientação de adulto) e mc-c04 (ofensas para ameaça a animal). Não alteradas as mensagens da implementação, os prompts ou as respostas históricas.

## Validação

75 testes Python e um teste JavaScript aprovados. O teste de seleção confere equilíbrio por chat e por grupo, estabilidade da seleção perante reordenação dos casos, correspondência dos formulários e ausência de julgamentos preenchidos. Nenhuma inferência de desenvolvimento ou final executada.

O PDF recompilado com Tectonic (motor XeTeX) tem 42 páginas. Foram conferidos os avisos de compilação e inspecionadas as páginas afetadas. A entrega Overleaf foi extraída e compilada separadamente. Não foi usado o serviço remoto Overleaf. Os avisos conhecidos de comentários de algorithm2e e versão de PDF das figuras não foram tratados como julgamentos de conteúdo ou certificação formal.

## Preservação

Casos reservados, referência humana, parecer primário, agenda original de desenvolvimento, resultados brutos, diagramas e congelamentos históricos preservados. Os arquivos da avaliação final permanecem prospectivos. A nota APLICACAO_AUDITORIA.md descreve a revisão anterior e não foi reescrita. O PDF e ZIP da raiz foram atualizados; o histórico anterior permanece no Git e nos backups existentes.

Pendentes: ratificação humana, confirmação de avaliadores, congelamento, execução final e julgamentos; automação de métricas compatível com este protocolo antes de seu uso. A revisão não demonstra eficácia, segurança geral ou adequação pedagógica.

## Continuação: cálculo automatizado

A pendência de automação descrita acima foi atendida por poc/final_metrics.py, com 30 testes novos (105 testes Python no total e um JavaScript). Ver CALCULO_ASCS_2026-11-04.md. Os indicadores finais permanecem dependentes de execução e revisão humana, ainda pendentes.
