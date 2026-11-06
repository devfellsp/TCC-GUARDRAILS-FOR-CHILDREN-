# Relatório de atualização e limpeza

Data: 05/11/2026 (America/Sao_Paulo).

## Sincronização com o GitHub

- Repositório: https://github.com/devfellsp/TCC-GUARDRAILS-FOR-CHILDREN-
- Branch: `main`.
- Estado inicial: `49e625c`, sem alterações locais pendentes.
- Estado atualizado: `570b711` — Atualiza TCC e PoC para GK-P2.6-dev com dez chats e diagramas Draw.io.
- Aplicado um commit por avanço direto (`fast-forward`), sem conflitos ou reescrita de histórico. Ao final da sincronização, zero commits locais ou remotos divergentes.
- Resumo recebido: 69 arquivos alterados, 3.201 linhas adicionadas e 151 removidas, além das mudanças em arquivos binários.

## Principais mudanças recebidas

1. **Protótipo GK-P2.6-dev:** dez chats — Português, Matemática, Ciências, História, Geografia, Arte, Educação Física, Inglês, Tecnologia e Geral. Novo iniciador `poc/Iniciar_GuardKids_Atual.cmd`, endereço local `http://127.0.0.1:8770`, busca restrita à matéria e restauração do índice preservado.
2. **Acervo:** quatro PDFs adicionados ao repositório. A seleção da versão atual reúne seis PDFs de quatro coleções e três sínteses anteriores, distribuídos em 40 blocos.
3. **TCC e entrega:** capítulos, referências, cronograma LaTeX, PDF final, pacote Overleaf e instruções atualizados. A nota de entrega recebida informa 44 páginas, oito figuras, dez tabelas e 24 referências; esses números não foram reavaliados visualmente nesta sincronização.
4. **Diagramas:** fontes Draw.io e PDFs de cinco diagramas atualizados, incluindo os arquivos conjuntos editáveis.
5. **Apresentação:** incluído `Apresentacao_TCC1_GuardKids_7min.pptx`.
6. **Histórico:** incluído `historico/Antes_atualizacao_TCC_GK_P2_6_20261105.zip`. A exclusão de `Cronograma.pdf` veio do GitHub; o cronograma vigente está em `texto/cronograma.tex`.
7. **Verificação:** novos testes Python e de interface para a ampliação por matéria.

## Limpeza realizada

Foram removidos **5.299 arquivos**, somando **228.825.280 bytes (218,22 MiB)** de conteúdo lógico, em **25 diretórios selecionados**. O espaço efetivamente liberado em disco pode variar conforme o sistema de arquivos.

- Temporários antigos de testes em `.cache/testes-*` e `.cache/v-precommit`.
- Caches de bytecode Python encontrados fora do ambiente virtual e dos backups em `.cache`.
- Temporários criados pelas verificações desta atualização.

Antes da remoção, os caminhos foram conferidos para permanecer dentro do projeto e os alvos iniciais foram confrontados com os arquivos versionados. Não foram removidos arquivos versionados pela limpeza local.

Foram preservados: `poc/.venv`, índices e dados locais, registros `runs`, evidências acadêmicas, versões anteriores, materiais didáticos, entregas, arquivos históricos, cópias de segurança, ferramentas de compilação e caches de compilação. Arquivos ignorados pelo Git não foram tratados automaticamente como lixo.

O inventário por diretório, com quantidades e tamanhos, está em [LIMPEZA_2026-11-05.json](LIMPEZA_2026-11-05.json).

## Verificações executadas

| Verificação | Resultado |
|---|---|
| Sincronização `HEAD` / `origin/main` | Zero commits divergentes |
| Restauração de estado preservado | 207 arquivos conferidos; três arquivos ausentes do índice GK-P2.6 criados; nenhuma sobrescrita e nenhuma inferência |
| Dependências Python (`pip check`) | Sem dependências quebradas |
| Suíte Python completa | **182 aprovados e um com falha**, em 55,68 segundos |
| Testes de interface Node | **Três aprovados** |
| Integridade do ZIP Overleaf | 283 entradas, nenhuma entrada corrompida, `main.tex` presente |
| `git diff --check` | Sem erros |

A primeira execução restrita da suíte Python ficou parada e foi interrompida. A execução completa acima foi realizada com acesso normal ao ambiente local. Não foram executadas novas consultas reais aos modelos nem recompilados os materiais acadêmicos.

### Divergência encontrada

O teste `poc/tests/test_corpus_expansion.py::test_baseline_files_and_runtime_remain_unchanged` falha ao conferir `ENTREGA_LEIA-ME.md` contra o manifesto histórico `poc/versions/GK-P2.1-dev/preservacao.json`.

- Hash esperado pelo manifesto: `94716f63c35945e451aab856e5579d14fbcad1975cea77fb8f320c04c1a7e395`.
- Hash encontrado: `b9519a569c7dffab94d5c98c688885bf4bcad1975cea77fb8f320c04c1a7e395`.

O arquivo de entrega foi alterado pelo próprio commit recebido do GitHub. A limpeza local não o modificou. O manifesto e o teste foram preservados: uma revisão posterior deve definir como conferir a preservação histórica diante das atualizações dos documentos de entrega. A suíte completa, portanto, **não está totalmente aprovada**.

## Estado final e pendências

O código e os documentos recebidos permanecem iguais ao commit `570b711`. Esta manutenção adicionou apenas este relatório e o inventário JSON, mantidos como arquivos locais novos, sem commit ou push.

Além da divergência do teste histórico, continuam as pendências científicas já declaradas na entrega: revisão humana dos recortes, conferência das condições de reutilização e replanejamento/congelamento da avaliação final para a ampliação. Esta sincronização não altera essas conclusões.
