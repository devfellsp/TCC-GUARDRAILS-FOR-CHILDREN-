# Cálculo prospectivo do ASCS

## Implementação

O módulo poc/final_metrics.py calcula ASCS conclusivo e por oportunidade, separados por estilo, chat e família. Trabalha com a agenda completa de 64 oportunidades, sem somar desenvolvimento ou histórico. A saída distingue sucesso, insucesso conclusivo, inconclusivo, pendência de revisão, perda técnica e oportunidade não executada. A comparação pareada usa somente decisões conclusivas nos dois estilos; resumos conclusivos de família exigem as duas formulações.

O programa lê os pareceres originais separadamente. Nos itens com segunda revisão, conserva os acordos e exige decisão documentada para cada dimensão divergente. Campos vazios não são tratados como julgamentos. A conferência documental não autentica a identidade do avaliador nem substitui a auditoria dos registros brutos.

Sem lote executado e revisão humana encerrada, as taxas finais ficam vazias. Em lote executado, o programa confere a referência ratificada, os hashes de casos/protocolo/referência no congelamento e a correspondência das oportunidades com a agenda. Não chama modelos, não gera respostas e não preenche pareceres.

## Verificação

30 testes novos cobrem sucesso integral, recusas indevidas com dimensões não aplicáveis, perda técnica, inconclusivo, campos humanos ausentes, divergência e conciliação, bloqueio de entradas contraditórias/duplicadas, famílias incompletas, lote parcial e leitura de um lote exclusivamente fictício de teste. A suíte completa passou com 105 testes Python e um teste JavaScript.

Com os arquivos reais atuais, o calculador informa 64 oportunidades não executadas e taxas finais nulas. Não foi executado o conjunto reservado. Casos, referências humanas, respostas históricas e julgamentos permanecem preservados.

## Documentação e apresentação

A metodologia e o guia do protocolo foram sincronizados com o novo calculador. A redação usa descrições neutras dos procedimentos de elaboração e inspeção preliminar; a revisão humana independente de conteúdo permanece pendente. O rótulo correspondente no diagrama de pesquisa foi atualizado, mantendo sua estrutura.

Uso: poc/.venv/Scripts/python.exe -B poc/final_metrics.py. Para lote final já executado: adicionar --batch e --reviews, conforme avaliacao/final_multichat_v1/README.md.

O registro REVISAO_PROTOCOLO_2026-11-04.md descreve a etapa anterior; sua pendência de automação do ASCS foi atendida nesta continuação.

O PDF de 42 páginas foi recompilado a partir de extração separada do ZIP e renderizado para conferência. Não há referências indefinidas, caracteres ausentes ou caixas excedendo as margens no log. O pacote foi conferido contra as fontes atuais.
