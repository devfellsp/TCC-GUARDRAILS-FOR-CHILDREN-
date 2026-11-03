# TCC GuardKids

Autor: Filipe Martins Henrique — UNITINS
Orientador: Prof. Marcos Souza

Guardrails configuráveis para uma prova de conceito de chatbot educativo infantil em português brasileiro, destinado a crianças de 7 a 11 anos.

## Arquivos atuais

- `document.tex`: versão principal da metodologia, trazida da pasta do Git em 25/10/2026. No Overleaf, selecione este arquivo como documento principal. As três cópias idênticas do texto foram consolidadas aqui.
- `ficha_tema_tcc_Filipe_Martins_Henrique_revisada.docx`: ficha de definição do tema.
- `Cronograma.pdf`: cronograma do projeto.
- `Livros_Didadicos/`: as duas apostilas educativas selecionadas, Trilhas (2021) e Livro do Estudante (2024).
- `artigos_e_guias/`: artigos científicos e guia de referência para as políticas de proteção.
- `benchmarks_e_datasets/`: MinorBench e planilhas do conjunto de dados de Martínez.
- `poc/`: implementação local do GuardKids, ambiente Python, configurações, seleção dos trechos, registros e documentação. Comece por `poc/LEIA-ME.md`.

## Executar o protótipo

Com o Ollama aberto, execute `poc/Iniciar_GuardKids.cmd` e abra http://127.0.0.1:8765. As perguntas iniciam sessões independentes. O protótipo está em desenvolvimento; os testes iniciais não são a avaliação final do TCC.

Os diagramas editáveis e as decisões estão em `poc/docs/ARQUITETURA_E_DECISOES.md`. O texto acadêmico `document.tex` ainda precisa ser atualizado a partir da implementação após a calibração.

## Histórico

- `historico/Historico_antes_da_organizacao_2026-10-25.zip`: cópia dos materiais locais anteriores à atualização, incluindo modelos, revisões e arquivos auxiliares. Guarde para recuperar algum conteúdo antigo, caso necessário.
- `historico/metodologia_guardkids_revisada.zip`: pacote recebido do Git, preservado como histórico; não foi regenerado a partir do texto atual.
- `historico/Capitulo_3_Metodologia_Versao_Anterior.pdf`: PDF da metodologia anterior.

A atualização copiou os arquivos da pasta recebida do Git e verificou a igualdade de conteúdo antes da limpeza. Em 03/11/2026, esta pasta foi conectada ao [repositório do projeto](https://github.com/devfellsp/TCC-GUARDRAILS-FOR-CHILDREN-), preservando o histórico existente e incluindo o código do protótipo em `poc/`. Ambientes locais, caches, índices gerados e registros individuais de execução ficam fora do versionamento; as decisões e os resumos do piloto estão em `poc/docs/`.
