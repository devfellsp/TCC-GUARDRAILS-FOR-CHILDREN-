# Materiais, evidências e reprodução

Documentação técnica de apoio, atualizada em 05/11/2026. Este guia reúne as instruções retiradas do antigo apêndice, sem integrar o manuscrito acadêmico.

## Alcance das entregas

| Material | Conteúdo |
| --- | --- |
| PDF da raiz | Manuscrito de 45 páginas; entregue separadamente, não incluído dentro do ZIP. |
| Overleaf_TCC_Drawio_rotulos.zip | Fontes editoriais, fontes tipográficas, sete figuras vetoriais e o cronograma em `texto/cronograma.tex` (`pgfgantt`), totalizando oito figuras. Inclui os suplementos de evidência descritos abaixo. |
| Implementação local | Código, dependências, modelos, fontes didáticas e índice compatível; necessários para executar o protótipo. |

O ZIP não inclui pesos dos modelos, ambiente Python instalado, livros didáticos integrais nem `poc/data/`. Não deve ser confundido com uma reprodução integral pronta para executar. O diretório genérico `poc/runs/` também fica fora do pacote: somente cópias selecionadas e conferidas dos registros fictícios são incluídas nas pastas de evidências. Não é necessário usar inferência para compilar o manuscrito ou conferir os registros.

## Compilação do manuscrito

No Overleaf, selecione `main.tex` e XeLaTeX. Preserve `texto/`, `generated/`, `fontes/` e `diagramas/`. O cronograma usa `pgfgantt`; os sete diagramas usam PDFs de `diagramas/pdf/`, com desenhos editáveis em `diagramas/drawio/`. Recompile até estabilizar listas e referências cruzadas. A entrega local foi compilada com Tectonic (motor XeTeX), sem submissão ao serviço remoto Overleaf.

## Lote multidisciplinar arquivado

A pasta `avaliacao/evidencias/multichat_20261104_revisado/` contém:

- `agenda.json`: registro original do planejamento anterior à execução; o status planejado foi preservado como evidência de origem.
- `resultados.csv`, `resumo.json`, `revisao_assistida_IA.json` e `REVISAO_DAS_RESPOSTAS.md`: resultados e inspeção preliminar originais, sem alteração dos campos humanos.
- `runs/`: cópias byte a byte dos 32 registros completos, identificados pelos `run_id` do CSV.
- `snapshots/`: cópia do snapshot indicado nesses registros, incluindo código, configuração, instruções, ambiente e índice do lote.
- `manifesto_rastreabilidade.json`: SHA-256 dos arquivos arquivados e relação entre lote, snapshot e índice.
- `ambiente_lote.json`: ambiente extraído dos registros e do snapshot, com a documentação complementar de hardware identificada separadamente.

Identificadores completos do lote:

- Versão: `GK-P2.1-dev`.
- Snapshot: `4531f5b01c5bc432a7c2ff8e67632c5e19cd0b8623ed414c89ec95731c4d3f8b`.
- Índice vetorial: `d68f62ab258c4ab93e36ef54df0e3626f6d4f191afcd59d52f38fefea755a344`.

O snapshot e o índice designam objetos diferentes. A identidade do snapshot é recalculada a partir de seu conteúdo JSON; os hashes do manifesto conferem os bytes das cópias. Isso verifica integridade, não independência da avaliação nem qualidade das respostas. As cópias arquivadas também permitem conferir as justificativas do verificador e os trechos recuperados citados no manuscrito.

Para conferir o arquivo de evidências existente, execute `python tools/archive_multichat_evidence.py` no ambiente do projeto. Quando o manifesto já existe, o comando apenas verifica o arquivo. Não chama modelos, não repete tentativas e não substitui cópias divergentes. Para empacotar as fontes e suplementos atuais, use `python tools/package_overleaf.py`.

## Ambiente registrado e interpretação dos tempos

| Componente | Registro |
| --- | --- |
| CPU de referência | AMD Ryzen 5 3600X, 6 núcleos e 12 processadores lógicos. |
| RAM de referência | 17.125.724.160 bytes, aproximadamente 16 GiB. |
| GPU disponível | NVIDIA GeForce RTX 4060; disponibilidade não comprova uso em todas as etapas. |
| Sistema do snapshot | `Windows-11-10.0.26300-SP0`. |
| Python do snapshot | 3.12.15; identificação completa em `ambiente_lote.json`. |
| Ollama nas execuções | 0.40.11. |

Digests dos modelos registrados nas execuções:

- `qwen3:8b`: `500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`.
- `bge-m3:latest`: `7907646426070047a77226ac3e684fbbe8410524f7b4a74d02837e43f2146bab`.

CPU, RAM e GPU provêm de `avaliacao/evidencias/ambiente_hardware.json`, uma conferência complementar do hardware local. Sistema e Python provêm do snapshot; Ollama e digests provêm dos registros das tentativas. Não houve monitoramento de hardware por tentativa nem comparação controlada de desempenho. Carga dos modelos, cache, rotas e quantidade de chamadas limitam a interpretação das latências. O registro `poc/docs/environment.json` também acompanha o pacote, como documentação anterior, sem substituir as identidades vinculadas ao lote.

## Estado local do índice e reconstrução

Na conferência de 05/11/2026, `poc/data/current.json` existe na pasta local e aponta para o índice identificado acima. Esse ponteiro não acompanha o ZIP editorial. A antiga observação de ponteiro ausente referia-se a outra cópia de trabalho e não descreve o estado atual.

Para reconstruir o índice, são necessários a implementação, as dependências, os PDFs e textos compatíveis com `poc/corpus_manifest.json` e os modelos no Ollama local. Execute `python poc/guardkids.py index` usando o ambiente da PoC. Confira o `id` em `poc/data/current.json` e os metadados e vetores em `poc/data/indices/<id>/`. Com o serviço iniciado, `/api/status` informa a prontidão e a identidade do índice validado. Essa operação é de reconstrução atual, não reprodução automática das inferências históricas. Não foi executada nesta revisão documental.

## Evidências históricas e protocolo reservado

O pacote inclui os dois lotes históricos em `avaliacao/evidencias/desenvolvimento_20261103_*/`, seus registros e snapshots, e os congelamentos em `avaliacao/congelamentos/`. As 108 execuções históricas de Ciências permanecem separadas das 32 tentativas atuais. O piloto de 22 execuções é preservado em `poc/docs/pilot_evidence.json`. Os materiais não foram reexecutados nem reinterpretados como um único experimento.

O plano de `avaliacao/final_multichat_v1/` contém 32 perguntas em 16 famílias, 64 oportunidades, 64 pareceres primários e 16 secundários. Os modelos de parecer, conciliação e comparação de clareza acompanham o pacote com campos humanos vazios. Identificação, datas e justificativas são preenchidas exclusivamente pelos responsáveis pela revisão. A ratificação das referências e o congelamento antecedem qualquer execução final. As instruções detalhadas estão no README do protocolo.

A execução final e os julgamentos continuam pendentes. O calculador `poc/final_metrics.py` não gera julgamentos: mantém as taxas finais vazias enquanto faltarem os requisitos do protocolo. A ocultação dos metadados das condições é parcial, pois o texto pode revelar o estilo.

## Geradores de documentação

`tools/update_manuscript.py` é um template histórico com a escrita desativada. Sua execução termina sem modificar `main.tex`. As fontes vigentes devem ser editadas diretamente. `tools/build_assets.py` conserva a geração das transcrições históricas e delega o pacote ao empacotador atual, evitando recriar a entrega antiga.
