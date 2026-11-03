# GuardKids — prova de conceito local

Abra `http://127.0.0.1:8765` com o serviço iniciado. O aplicativo só aceita conexões do próprio computador. Não é necessário criar conta, nem contratar API.

## Iniciar novamente

1. Abra o Ollama.
2. Execute `Iniciar_GuardKids.cmd` nesta pasta e mantenha a janela aberta.
3. Abra `http://127.0.0.1:8765` no navegador. Para encerrar, use Ctrl+C na janela do serviço.

Se o serviço tiver sido iniciado em segundo plano, execute `parar.ps1` para encerrá-lo. O serviço não foi configurado para iniciar com o Windows. O modelo pode precisar de uma primeira chamada mais lenta para carregar os pesos.

O ambiente `.venv` foi criado a partir do Python 3.12 do Anaconda existente, sem instalar pacotes no ambiente base. Os pesos dos modelos ficam no armazenamento padrão do Ollama, fora da pasta do TCC. O restante da implementação está aqui.

## Organização

| Arquivo/pasta | Função |
|---|---|
| `config.json` | Modelo, geração, busca e configurações de proteção |
| `corpus_manifest.json` | Fontes, páginas, âncoras de extração e exclusões justificadas |
| `prompts/` | Instruções independentes de classificação e geração |
| `guardkids.py` | Extração, indexação, busca e fluxo das perguntas |
| `app.py`, `web/` | Interface local e API |
| `data/` | Trechos extraídos e vetores de busca |
| `runs/` | Um registro completo por execução e CSVs para análise humana |
| `development_cases.json` | Perguntas exclusivas de desenvolvimento, não de avaliação final |
| `run_development.py` | Execução das perguntas nas configurações escolhidas |
| `tests/` | Testes da lógica, sem medir a eficácia do modelo |
| `docs/` | Decisões, diagramas e evidências de funcionamento |
| `requirements-lock.txt` | Versões exatas dos pacotes instalados |

## Comandos de manutenção

No PowerShell, dentro desta pasta:

```powershell
# Refazer a base após uma alteração de páginas, PDFs, embeddings ou busca
.\.venv\Scripts\python.exe guardkids.py index

# Pergunta isolada
.\.venv\Scripts\python.exe guardkids.py ask "Qual é o papel dos decompositores?"

# Piloto de desenvolvimento nas duas configurações
.\.venv\Scripts\python.exe run_development.py --policies ajustada referencia

# Testes da lógica
.\.venv\Scripts\python.exe -m pytest -q
```

Para recriar o ambiente: use o Python 3.12 para criar `.venv`, instale `requirements-lock.txt`, baixe `qwen3:8b` e `bge-m3` pelo Ollama e reconstrua o índice. A documentação da metodologia deve citar os digests registrados, pois as tags dos modelos podem mudar.

## O que o piloto demonstra

O fluxo usa classificação contextual de entrada, recuperação vetorial, geração com indicação de fontes e classificação de saída. Decisões são aplicadas pela lógica de configuração. Respostas rejeitadas não são enviadas à interface, mas permanecem nos registros do pesquisador. Falhas de rede, modelo, JSON e citações são perdas técnicas, sem serem contadas como proteção bem-sucedida.

`referencia` é uma configuração experimental conservadora que bloqueia predação educativa quando identificada. `ajustada` permite esse contexto, preservando o bloqueio de instruções para dano. Essa diferença foi escolhida para o piloto e ainda deve ser justificada e congelada na calibração antes do experimento final. A referência não representa necessariamente a melhor configuração possível.

Uma citação existente não prova que a resposta está correta nem que todas as suas afirmações estão sustentadas. O próprio modelo decide se encontrou apoio suficiente e participa dos guardrails; suas falhas podem ser correlacionadas. A revisão humana continua necessária.

O corpus é pequeno e intencional. As condições de reutilização das obras e trechos de terceiros ainda precisam ser documentadas antes de qualquer distribuição pública. Os PDFs não são expostos pelo servidor. Não há participação de crianças neste piloto. Use somente perguntas fictícias: as perguntas e respostas são gravadas em texto no computador.

## Antes da avaliação final

- Conferir políticas e casos com o orientador, incluindo solicitações de risco, ambiguidades e perguntas fora do acervo.
- Fixar amostra, quantidade de repetições, configuração de referência, ajuste e critérios de inclusão/exclusão.
- Separar rigorosamente desenvolvimento e avaliação; não reutilizar o pequeno piloto como evidência final de eficácia.
- Congelar e identificar código, prompts, modelos, corpus e parâmetros.
- Revisar manualmente conteúdo inadequado, bloqueios indevidos, correção, pertinência e clareza. O CSV do piloto deixa esses campos vazios de propósito.
- Comparar casos correspondentes e reportar erros técnicos e julgamentos inconclusivos, além dos numeradores e denominadores dos indicadores.
