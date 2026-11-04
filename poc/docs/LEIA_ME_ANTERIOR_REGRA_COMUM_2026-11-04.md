# GuardKids — prova de conceito local

## Linguagem da resposta — 04/11/2026

O seletor **Como você quer a explicação?** oferece `Direto` e `Passo a passo · com exemplos`. A interface inicia em passo a passo: resposta simples, duas ou três etapas curtas e exemplo sustentado no acervo, dentro das mesmas 120 palavras. A orientação evita jargão desnecessário e voz de bebê. Está disponível nos quatro chats.

É uma política de apresentação independente da política de proteção (`referencia`/`ajustada`). Não muda o perfil fictício, a busca, os critérios de bloqueio nem as verificações de fontes e segurança. As orientações fixas de cuidado permanecem iguais. A escolha e seu hash são registrados; as definições entram no snapshot. O estilo é uma instrução ao modelo, não garantia automática de compreensão ou clareza.

API e executores anteriores preservam `padrao` quando o estilo é omitido. Exemplo de desenvolvimento: `poc/.venv/Scripts/python.exe poc/guardkids.py ask "Por que uma bola faz sombra?" --channel geral --response-style passo_a_passo --synthetic`. O executor `run_development.py` também aceita `--response-style`. Ao comparar estilos, manter pergunta, fontes, perfil e política de proteção iguais e registrar clareza, correção e sustentação separadamente. A comparação de linguagem não altera o desenho da comparação original entre proteções.

As respostas da sondagem de linguagem ficam em `docs/response_styles_smoke_2026-11-04.json`. São exemplos de desenvolvimento, sem avaliação com crianças ou ratificação pedagógica independente.

## Quatro chats — desenvolvimento de 04/11/2026

A interface permite escolher **Ciências, História, Geografia e Geral**. O Geral cobre organização cotidiana, convivência, privacidade e curiosidades presentes no pequeno acervo. Todos usam o mesmo perfil fictício de nove anos e as mesmas verificações de entrada, sustentação e saída. As perguntas continuam independentes, sem memória de conversa. A busca filtra a disciplina antes de escolher os trechos.

Ciências conserva as fontes didáticas anteriores. Os três novos acervos em `corpus/` são textos experimentais produzidos com assistência de IA, identificados como rascunhos e **pendentes de revisão pedagógica e factual independente**. Não representam cobertura integral das matérias. Não se responde com conhecimento livre quando faltam fontes.

`multichat_cases.json` contém 16 casos fictícios de desenvolvimento: quatro por chat (pergunta legítima, fora do acervo, risco e ajuda). As ações esperadas são propostas para revisão, não julgamentos de eficácia. Para executar o lote: `poc/.venv/Scripts/python.exe poc/run_development.py --suite multichat --policies ajustada`, a partir da raiz. Para uma pergunta isolada: `poc/.venv/Scripts/python.exe poc/guardkids.py ask "O que são fontes históricas?" --channel historia --synthetic`.

Depois de alterar fontes, execute `poc/.venv/Scripts/python.exe poc/guardkids.py index`. Inicie a interface como descrito abaixo. Detalhes e limites: `docs/QUATRO_CHATS_2026-11-04.md`.

Esta ampliação é uma etapa de desenvolvimento separada do protocolo prospectivo de Ciências documentado abaixo. Os congelamentos anteriores e suas evidências permanecem preservados; o índice novo recebe outro identificador. O protocolo, o texto acadêmico e o conjunto reservado não foram convertidos automaticamente em avaliação multidisciplinar. A diferença entre políticas continua sendo exclusivamente a predação educativa: não é uma comparação específica de políticas de História, Geografia ou Geral.

Versão do projeto acadêmico: **Projeto/TCC I**, código GK-P1.2. Protocolo em `../avaliacao/PROTOCOLO.md`, rubrica, 40 perguntas reservadas e referências humanas pendentes. O executor `evaluation.py` separa desenvolvimento e avaliação final condicionada à ratificação. Os lotes novos preservam falhas de classificação e sustentação; não há eficácia ou segurança geral demonstrada.

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
| `data/current.json`, `data/indices/<id>/` | Ponteiro e versões completas do índice validado |
| `runs/` | Registros minimizados; conteúdo completo apenas em execuções explicitamente fictícias |
| `privacy.py`, `settings.py` | Minimização dos registros e validação da configuração |
| `experiment.py` | Exportação de experimentos fictícios e resumo condicionado a julgamento humano |
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

# Migrar o índice anterior, validando-o contra os PDFs, sem chamar o modelo
.\.venv\Scripts\python.exe guardkids.py migrate-index

# Pergunta isolada
.\.venv\Scripts\python.exe guardkids.py ask "Qual é o papel dos decompositores?"

# Piloto de desenvolvimento nas duas configurações
.\.venv\Scripts\python.exe run_development.py --policies ajustada referencia

# Testes da lógica
.\.venv\Scripts\python.exe -m pytest -q
```

Para recriar o ambiente: use o Python 3.12 para criar `.venv`, instale `requirements-lock.txt`, baixe `qwen3:8b` e `bge-m3` pelo Ollama e reconstrua o índice. A documentação da metodologia deve citar os digests registrados, pois as tags dos modelos podem mudar.

## O que o piloto demonstra

O fluxo usa classificação contextual de entrada, recuperação vetorial, geração com indicação de fontes e classificação de saída. Decisões são aplicadas pela lógica de configuração. Respostas rejeitadas não são enviadas à interface. Falhas de rede, modelo, JSON e citações são perdas técnicas, sem serem contadas como proteção bem-sucedida.

Na versão revisada, uma verificação adicional de sustentação ocorre antes da inspeção de segurança da saída; também usa Qwen3, não é independente e pode errar. O código aplica o limite de 120 palavras. A detecção local de alguns identificadores explícitos pode interromper a pergunta antes do modelo, mas não detecta todos os dados pessoais.

`referencia` é uma configuração experimental conservadora que bloqueia predação educativa quando identificada. `ajustada` permite esse contexto, preservando o bloqueio de instruções para dano. Essa diferença foi escolhida para o piloto e ainda deve ser justificada e congelada na calibração antes do experimento final. A referência não representa necessariamente a melhor configuração possível.

Uma citação existente não prova que a resposta está correta nem que todas as suas afirmações estão sustentadas. O próprio modelo decide se encontrou apoio suficiente e participa dos guardrails; suas falhas podem ser correlacionadas. A revisão humana continua necessária.

O corpus é pequeno e intencional. As condições de reutilização das obras e trechos de terceiros ainda precisam ser documentadas antes de qualquer distribuição pública. Os PDFs não são expostos pelo servidor. Não há participação de crianças neste piloto. Use somente perguntas fictícias. Os novos registros da interface omitem pergunta, resposta gerada e justificativas livres; a resposta liberada é exibida durante a tentativa. Não há cadastro ou armazenamento de histórico no navegador.

## Registros, retenção e exportação

Somente `run_development.py`, que usa os casos fictícios locais, ou `guardkids.py ask --synthetic` habilitam registros integrais. A API não aceita esse parâmetro. Esse modo é uma declaração explícita do pesquisador, não uma detecção automática de que os dados são fictícios. Não o utilize com dados reais. Rascunhos rejeitados são preservados integralmente apenas nesse modo.

O prazo configurado para registros comuns é de 30 dias. Confira candidatos à expiração com `python guardkids.py prune`; aplique com `python guardkids.py prune --apply`. O procedimento afeta apenas novos registros marcados como minimizados; registros legados, CSVs de pesquisa e snapshots permanecem preservados. A manutenção deve ser executada pelo pesquisador; não existe exclusão automática em segundo plano. Restrinja o acesso à pasta no sistema operacional. Registros históricos não foram apagados nem anonimizados retroativamente.

O snapshot reúne código, prompts, configuração, ambiente instalado e índice quando disponível. Para exportar execuções explicitamente fictícias: `python experiment.py export --run-ids ID1 ID2 --output runs/experimento.zip`. O pacote não inclui pesos nem PDFs originais e deve ter seus direitos de reutilização revisados antes de redistribuição. `python experiment.py summary runs/arquivo.csv` mantém a taxa de conteúdo inadequado pendente enquanto faltarem julgamentos, justificativas, avaliador e data.

## Prontidão e concorrência

`/api/status` valida modelos e índice, inclusive texto, páginas, hashes, dimensões e normalização. `/api/health` informa apenas que o processo está vivo. Hosts e origens de navegador são restritos aos endereços locais na porta 8765; o corpo da pergunta tem limite de 8 KiB. Clientes locais sem cabeçalho Origin continuam aceitos para uso pelo pesquisador.

A aplicação processa uma pergunta por vez; outras recebem 429 em vez de aguardar numa fila. O orçamento de inferência é de 120 segundos por tentativa, configurável em `runtime.deadline_seconds`; cada operação de rede usa o orçamento restante. Cancelamento e prazo são conferidos entre etapas e durante a leitura da resposta. Uma chamada de rede já em espera pode terminar somente ao responder ou atingir o timeout; o cancelamento não descarrega o modelo do Ollama. Falha na escrita do registro retém a resposta e retorna 503.

## Texto acadêmico e evidências

O piloto de 25/10/2026 foi preservado em `docs/pilot_evidence.json`, com apenas casos fictícios conferidos, ações, fontes, tempos e identificadores. Os julgamentos humanos continuam pendentes. Os tempos históricos não medem a versão revisada, que tem uma chamada adicional ao modelo. A carga a frio de aproximadamente 79 segundos pertence a outra rodada. Consulte `docs/CORRECOES_2026-11-03.md` para a correspondência entre problemas e correções.

## Antes da avaliação final

- Conferir políticas e casos com o orientador, incluindo solicitações de risco, ambiguidades e perguntas fora do acervo.
- Fixar amostra, quantidade de repetições, configuração de referência, ajuste e critérios de inclusão/exclusão.
- Separar rigorosamente desenvolvimento e avaliação; não reutilizar o pequeno piloto como evidência final de eficácia.
- Congelar e identificar código, prompts, modelos, corpus e parâmetros.
- Revisar manualmente conteúdo inadequado, bloqueios indevidos, correção, pertinência e clareza. O CSV do piloto deixa esses campos vazios de propósito.
- Comparar casos correspondentes e reportar erros técnicos e julgamentos inconclusivos, além dos numeradores e denominadores dos indicadores.
