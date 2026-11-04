# GuardKids — prova de conceito local

## Versão atual: GK-P2.1-dev — 04/11/2026

A POC tem quatro chats: Ciências, História, Geografia e Geral. Usa um perfil fictício de nove anos, com perguntas independentes e sem participação de crianças. Esta é uma etapa de desenvolvimento; não há eficácia educativa nem segurança geral demonstrada.

**Regra de proteção:** uma regra educativa comum aos quatro chats. Permite conteúdo educativo apoiado no acervo, inclusive predação não gráfica; intervém em pedidos prejudiciais; oferece orientação fixa de cuidado em pedidos de ajuda; informa falta de apoio quando as fontes não sustentam uma resposta. As verificações podem errar. Privacidade e autolesão recebem orientação fixa conforme a decisão já existente.

**Estilo da explicação:** Direto (`padrao`) ou Passo a passo (`passo_a_passo`). O segundo é a escolha inicial da interface: frase simples, duas etapas e exemplo, até 120 palavras. O estilo orienta a geração, não muda o critério de proteção. Exemplos também precisam de apoio nas fontes. API e linha de comando usam `padrao` quando o estilo é omitido, preservando a escolha explícita nos registros de pesquisa.

A interface mostra “Regra de proteção”, com uma explicação da regra comum. O seletor anterior entre Referência e Ajustada foi removido. A API atual aceita apenas `comum` como regra explícita, ou usa essa regra por padrão.

## Iniciar e parar

Com o Ollama aberto, execute `poc/Iniciar_GuardKids.cmd` e acesse http://127.0.0.1:8765. O servidor é local, sem cadastro. Para parar, use Ctrl+C na janela do serviço ou `poc/parar.ps1` se iniciado em segundo plano. Na etapa de pesquisa de 04/11/2026, somente o Ollama foi usado para 32 tentativas; o servidor da interface não foi iniciado.

## Casos e comparação de linguagem

`multichat_cases.json` tem 16 perguntas fictícias assistidas por IA: quatro por chat, cobrindo conteúdo educativo, falta de apoio, risco e ajuda. As ações esperadas são propostas para revisão. A comparação aplica as mesmas perguntas, fontes, perfil, modelo e regra comum aos dois estilos. A ordem das perguntas é embaralhada com semente fixa; o primeiro estilo alterna para equilibrar sua posição. São 32 tentativas planejadas, sem repetição técnica adicional e sem equivaler a 32 perguntas independentes.

A partir da raiz do projeto:

```powershell
# Preparar agenda sem chamar o modelo ou iniciar a POC
poc/.venv/Scripts/python.exe poc/run_development.py --plan

# Executar desenvolvimento somente quando desejar usar o modelo local
poc/.venv/Scripts/python.exe poc/run_development.py --suite multichat

# Testar um único estilo
poc/.venv/Scripts/python.exe poc/run_development.py --response-style passo_a_passo

# Pergunta isolada declaradamente fictícia
poc/.venv/Scripts/python.exe poc/guardkids.py ask "Por que uma bola faz sombra?" --channel geral --policy comum --response-style passo_a_passo --synthetic
```

Cada lote recebe uma pasta nova. A agenda é gravada antes das tentativas; os resultados são persistidos após cada uma. Falhas técnicas permanecem registradas, sem repetição seletiva. Os campos de julgamento humano ficam vazios. Não usar o resumidor histórico de comparação entre políticas para agrupar esses resultados: o contraste atual é entre estilos, dentro da mesma regra.

Plano atual: `../avaliacao/PROTOCOLO_MULTICHAT_DESENVOLVIMENTO.md`. Lote revisado executado: `../avaliacao/evidencias/multichat_20261104_revisado/`. As 32 tentativas concluíram sem perdas técnicas; inspeção assistida apontou ressalvas de sustentação em cinco das oito explicações liberadas. Ver `REVISAO_DAS_RESPOSTAS.md` nessa pasta. As rotas coincidiram com a referência proposta, sem equivaler a qualidade de conteúdo.

## Fontes, funcionamento e registros

A busca seleciona apenas trechos do chat escolhido antes de aplicar o top-k. Ciências usa as duas fontes didáticas anteriormente selecionadas. História, Geografia e Geral usam os pequenos textos de `corpus/`, assistidos por IA e pendentes de revisão pedagógica e factual independente. Esses textos foram revisados com fontes externas identificadas no manifesto, mantendo a condição de sínteses experimentais assistidas por IA; não representam cobertura integral das matérias. O Geral também depende do acervo, sem pesquisa livre na internet.

O fluxo conserva proteção de entrada, busca, geração, verificação de sustentação e proteção de saída. Respostas rejeitadas não são enviadas ao navegador. O mesmo modelo participa das verificações; elas não são julgamentos independentes. Já houve acréscimos sem apoio liberados pelo verificador em sondagens anteriores, preservados nos registros.

Registros comuns omitem o texto livre; dados integrais são exclusivos de tentativas declaradas fictícias pelo executor. Não usar `--synthetic` com dados reais. O estilo, a regra, o chat, os hashes e o snapshot identificam a condição usada. A detecção local de alguns dados pessoais não detecta todos os identificadores. A retenção configurada dos registros minimizados é de 30 dias; `guardkids.py prune` lista candidatos e `prune --apply` aplica a exclusão. Não há limpeza automática em segundo plano; evidências históricas e registros sintéticos são preservados.

O serviço processa uma pergunta por vez e mantém prazo global de 120 segundos. Erros de modelo, índice, prazo, JSON, citações e persistência são falhas técnicas, não recusas corretas. A falta de apoio pode ser comunicada sem gerar resposta factual.

Para refazer o índice após alterar fontes ou recuperação: `poc/.venv/Scripts/python.exe poc/guardkids.py index`. O índice foi reconstruído após a revisão das sínteses e é identificado no snapshot do lote. Não alterar as fontes para tornar retrospectivamente apoiadas as respostas produzidas.

## Verificação e histórico

Execute `poc/.venv/Scripts/python.exe -m pytest poc/tests -q` e `node --test poc/tests/test_web.cjs`. São verificações de funcionamento; não medem compreensão por crianças.

Os protocolos, resultados, PDFs e congelamentos anteriores foram preservados. `evaluation.py` pertence ao desenho anterior entre Referência e Ajustada e rejeita execução de seus procedimentos com a configuração atual. Suas funções de leitura e análise histórica permanecem disponíveis. O manuscrito, os diagramas internos e o PDF foram atualizados para distinguir o desenho atual do histórico. A avaliação final proposta está em `../avaliacao/final_multichat_v1/README.md`, com 32 perguntas, 64 oportunidades, ratificação humana e congelamento obrigatórios. O executor é `final_multichat.py`; os casos reservados não foram executados.

Documentação anterior preservada em `docs/LEIA_ME_ANTERIOR_REGRA_COMUM_2026-11-04.md`. Relatório desta revisão em `docs/RELATORIO_REGRA_COMUM_2026-11-04.md`.

Relatório da etapa de pesquisa: `docs/RELATORIO_PESQUISA_2026-11-04.md`. O relatório da alteração inicial da regra comum é histórico e permanece preservado.
