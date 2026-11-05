# GuardKids GK-P2.2-dev — acervo ampliado de desenvolvimento

Esta execução é separada da GK-P2.1-dev usada no TCC. A ampliação não foi incorporada ao PDF de 41 páginas, ao pacote Overleaf ou à apresentação. Nenhum arquivo da versão anterior precisa ser substituído para selecionar esta versão.

## Selecionar a versão

Na raiz do projeto, com Ollama disponível e os modelos locais instalados:

```powershell
# Nova versão: interface identificada, em porta própria
poc/versions/GK-P2.2-dev/Iniciar_GK_P2_2.cmd
# Abrir http://127.0.0.1:8766

# Consulta isolada (a marca --synthetic deve ser usada somente com perguntas fictícias)
poc/.venv/Scripts/python.exe -B poc/versions/GK-P2.2-dev/guardkids.py ask "O que são serviços de hotelaria no texto sobre o campo?" --channel historia --policy comum --response-style padrao --synthetic
```

Use uma versão por vez para evitar disputa de recursos dos modelos. As perguntas da interface continuam sem memória entre tentativas. A interface mantém exemplos herdados; os novos assuntos estão relacionados em SELECAO_DO_ACERVO.md. A regra comum, os parâmetros, os prompts e as descrições textuais de escopo foram mantidos como controles desta ampliação; as descrições herdadas não enumeram todos os novos temas e podem ser refinadas em uma próxima revisão documentada. A classificação de cada recorte segue a disciplina do livro. A presença de uma fonte não garante que a busca, o gerador ou os verificadores acertem.

## Acervo e recuperação

Há 18 blocos: Ciências 5, História 6, Geografia 6 e Geral 1. Foram acrescentados dez recortes literais do livro local do quarto ano, com páginas, âncoras, assunto, motivo e hashes. Os oito blocos antigos continuam presentes, sem alteração de texto ou identificador. A nova extração exige disciplina explícita e hash da fonte, confere hashes dos recortes novos e rejeita IDs duplicados. O filtro de chat continua anterior ao top-k.

As sínteses anteriores de História, Geografia e Geral foram mantidas; a ampliação não certifica suas adaptações. A seleção dos novos recortes é documental e preliminar, sem revisão pedagógica independente. O livro e suas imagens não foram duplicados na pasta da versão. Consulte SELECAO_DO_ACERVO.md para a comparação e as exclusões.

## Índice e rastreabilidade

O índice ativo desta versão fica somente em `poc/versions/GK-P2.2-dev/data/`, separado de `poc/data/`. Sua cópia preservada fica em `indice_preservado/`, com o ponteiro e os arquivos de metadados/vetores identificados pelo mesmo hash. Para restaurar a cópia preservada desta versão, sem inferência:

```powershell
poc/.venv/Scripts/python.exe -B poc/versions/GK-P2.2-dev/restore_index.py
```

Para reconstruir a partir das fontes, somente quando necessário:

```powershell
poc/.venv/Scripts/python.exe -B poc/versions/GK-P2.2-dev/guardkids.py index
```

Reconstrução pode gerar novo índice e exige novo plano antes de inferências de pesquisa. Não altera o índice da raiz. Os logs completos desta versão ficam em sua própria pasta `runs/`; o lote executado é arquivado fora da pasta ignorada, em `avaliacao/evidencias/ampliacao_GK_P2_2_dev_20261105/`, com os registros e o snapshot original. As instruções de execução do lote são `run_expansion.py plan` e `run_expansion.py run`; um lote já iniciado não pode ser repetido por esses comandos.

## Recuperar a versão do TCC

A GK-P2.1-dev continua selecionada pelos comandos originais, por exemplo `poc/Iniciar_GuardKids.cmd`, na porta 8765. Encerre a interface ampliada antes de iniciar a anterior. O código, configuração, manifesto e índice originais na raiz não foram alterados.

As cópias de configuração, manifesto, código, prompts e interface estão em `poc/versions/GK-P2.1-dev/originais/poc/`. O índice preservado está em `poc/versions/GK-P2.1-dev/indice_preservado/`. Não execute o código diretamente da pasta `originais`: ela conserva os bytes e caminhos para eventual reposição nos locais originais. Se for necessária uma recuperação posterior, primeiro compare os hashes em preservacao.json e então reponha os arquivos nos caminhos registrados. O ponteiro e os metadados/vetores devem ser recuperados em conjunto; índice e snapshot são identificadores diferentes.

Para conferir a preservação atual, sem alterar arquivos:

```powershell
poc/.venv/Scripts/python.exe -B poc/versions/verificar_preservacao.py
```

## Avaliação e limites

Leia `RELATORIO_DESENVOLVIMENTO.md` para os resultados efetivos: 121 testes Python e um JavaScript aprovados, 32 tentativas reais sem perdas técnicas, com limitações de sustentação e redação preservadas. Para auditar o lote sem inferência, execute na raiz `poc/.venv/Scripts/python.exe -B poc/versions/verificar_ampliacao.py`. O manifesto de integridade do lote fica em sua pasta de evidências.

O conjunto reservado existente não foi executado, alterado ou liberado. Leia IMPACTO_PLANO_FINAL.md antes de planejar qualquer avaliação da nova versão. Os resultados de desenvolvimento pertencem à GK-P2.2-dev e não devem ser somados aos 32 registros atuais do TCC, aos 108 históricos ou às 64 oportunidades finais planejadas. A inspeção preliminar não equivale à revisão humana independente. A ampliação não demonstra segurança, compreensão infantil ou eficácia educativa.
