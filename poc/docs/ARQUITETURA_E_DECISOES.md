# Arquitetura e decisões — piloto de 25/10/2026 e revisão de 03/11/2026

Este documento descreve a implementação inicial para desenvolvimento. Os diagramas são fontes editáveis para posterior adaptação à metodologia. Não descrevem uma avaliação final concluída.

## 1. Etapas da pesquisa

```mermaid
flowchart TD
    A[Revisar referências e delimitar o cenário] --> B[Definir políticas e tratamentos esperados]
    B --> C[Selecionar trechos e documentar fontes]
    C --> D[Construir o protótipo e os registros]
    D --> E[Calibrar com perguntas de desenvolvimento]
    E --> F[Fixar configurações, amostra e rubrica]
    F --> G[Executar avaliação independente nas duas configurações]
    G --> H[Julgar respostas e comparar indicadores]
    H --> I[Discutir resultados, falhas e limites]
```

As políticas orientam a implementação e o julgamento. A calibração permite corrigir o protótipo sem contaminar a avaliação final: perguntas usadas nessa etapa não integram a amostra final. O estágio de congelamento impede escolher regras depois de observar o desempenho nas perguntas finais. No momento, o projeto está em construção e calibração.

## 2. Arquitetura do protótipo

```mermaid
flowchart TD
    P[Pergunta em sessão independente] --> X[Detecção parcial de identificadores explícitos]
    X -- Identificador detectado --> M[Orientação segura de privacidade]
    X -- Sem detecção --> E[Qwen3: classificação contextual de entrada]
    E --> D{Política permite?}
    D -- Não --> M[Mensagem fixa de proteção ou cuidado]
    D -- Sim --> V[BGE-M3 em CPU: vetor da pergunta]
    V --> R[Busca por similaridade cosseno: até 3 trechos]
    R --> C{Há trechos acima do limiar?}
    C -- Não --> I[Mensagem de insuficiência do acervo]
    C -- Sim --> G[Qwen3: resposta educativa em JSON e IDs das fontes]
    G --> A{Modelo indica apoio e cita IDs válidos?}
    A -- Sem apoio --> I
    A -- Citação inválida --> T[Erro técnico registrado]
    A -- Sim --> V2[Qwen3: verificação adicional de sustentação]
    V2 -- Sem apoio --> I
    V2 -- Apoio indicado --> S[Qwen3: classificação contextual da saída]
    S --> O{Política permite a resposta?}
    O -- Não --> M
    O -- Sim --> F[Resposta educativa com páginas das fontes]
    M --> L[Registro minimizado ou sintético explícito]
    I --> L
    F --> L
    T --> L
```

A recuperação usa somente os parágrafos selecionados no manifesto. O índice local guarda vetores e metadados em data/indices/<id>/; data/current.json aponta para uma versão completa. A leitura valida hashes, texto e metadados contra a extração dos PDFs, normalizando espaços. O BGE-M3 executa em CPU para reservar memória da GPU ao Qwen3 8B. A geração é orientada pelo perfil fixo de 9 anos/4º ano e tem temperatura zero, semente 42, top-p 0,9 e contexto de 4096 tokens. Essas opções reduzem variação, mas não garantem determinismo entre versões ou equipamentos.

Classificação, geração e verificação adicional de sustentação são chamadas separadas do mesmo Qwen3, com instruções e esquema de saída diferentes. Isso simplifica a execução local, mas não equivale a uma validação independente. Os registros distinguem decisões de entrada, ausência de fonte, indicação de insuficiência pelo gerador e proteção de saída. A recusa feita pelo próprio modelo também precisa ser reconhecida na análise humana.

## 3. Aplicação das políticas

```mermaid
flowchart TD
    A[Categoria, necessidade de proteção e contexto educativo] --> B{Exige proteção?}
    B -- Sim --> C{Autolesão, privacidade ou ajuda reconhecida em perigo, sexual, ofensa ou substância?}
    C -- Sim --> D[Orientação de cuidado previamente definida]
    C -- Não --> E[Bloqueio com mensagem previamente definida]
    B -- Não --> F{Predação educativa identificada?}
    F -- Não --> G[Permitir o fluxo]
    F -- Sim --> H{Configuração permite predação educativa?}
    H -- Sim --> G
    H -- Não --> E
```

A necessidade de proteção tem precedência: um pedido de instruções para ferir animais deve permanecer bloqueado mesmo que mencione cadeias alimentares. A configuração ajustada muda somente a permissão de predação educativa. A classificação automática pode errar ambas as distinções, por isso as decisões ficam disponíveis para julgamento posterior. O limiar de similaridade 0,45 é um parâmetro provisório da busca, não uma probabilidade de segurança ou correção.

## 4. Protocolo da comparação

```mermaid
flowchart TD
    A[Perguntas finais classificadas antes das respostas] --> B[Mesma pergunta e perfil em sessões independentes]
    B --> C[Configuração de referência]
    B --> D[Configuração ajustada]
    C --> E[Registros com versões, fontes e decisões]
    D --> E
    E --> F[Separar execuções válidas, falhas técnicas e inconclusivos]
    F --> G[Julgamento humano por políticas e rubrica]
    G --> H[Comparação por pergunta, grupo e categoria]
    H --> I[Respostas inadequadas, bloqueios indevidos e qualidade]
```

O piloto atual exporta perguntas e respostas, mas não preenche julgamentos de segurança ou qualidade automaticamente. A classificação usada pelo guardrail não será usada como verdade de referência. Os critérios definidos no capítulo de metodologia orientarão os numeradores e denominadores. Até o congelamento do protocolo, toda execução é desenvolvimento.

## Escolhas e pendências

| Item | Situação inicial |
|---|---|
| Modelo gerador e verificador | Qwen3 8B Q4_K_M no Ollama, sem treino dos pesos |
| Embeddings | BGE-M3, vetores normalizados de 1024 dimensões, execução em CPU |
| Armazenamento | NumPy local; cinco trechos, versões publicadas antes da troca do ponteiro ativo |
| Corpus | Uma passagem do Trilhas e quatro do Livro do Estudante de SP |
| Fragmentação | Limite rígido de 850 caracteres; sobreposição reduzida se não houver espaço |
| Busca | Até três resultados, similaridade cosseno mínima provisória de 0,45 |
| Interface | FastAPI e HTML local, endereço 127.0.0.1:8765 |
| Categorias | Dano, autolesão, sexual, ódio/ofensas, substâncias, privacidade e tentativa de substituir instruções |
| Fora do acervo | Busca e declaração de apoio insuficiente pelo gerador, sem garantia de detecção perfeita |
| Registro | Texto livre omitido por padrão; conteúdo integral apenas em execução declarada fictícia, com configurações, hashes e durações |
| Avaliação final | Ainda não executada; faltam amostra, repetições, revisão das políticas e congelamento |
| Reutilização das obras | Condições e créditos de terceiros ainda precisam de documentação para distribuição |

## Documentação técnica consultada

- [Qwen3 8B no Ollama](https://ollama.com/library/qwen3:8b): tamanho, quantização e licença do pacote.
- [BGE-M3 no Ollama](https://ollama.com/library/bge-m3): embeddings multilíngues.
- [API de embeddings](https://docs.ollama.com/api/embed): vetorização local.
- [Saídas estruturadas](https://docs.ollama.com/capabilities/structured-outputs): esquema JSON e validação.
- [Controle de pensamento](https://docs.ollama.com/capabilities/thinking): desativação explícita durante as chamadas.

## Revisão de segurança

A API valida hosts e origens locais, limita o corpo a 8 KiB e não aceita habilitação de logs integrais. Uma pergunta é processada por vez; concorrência recebe 429. Falha na persistência retém a resposta. O orçamento de inferência padrão é 120 s; uma operação de rede em espera pode terminar ao responder ou ao atingir seu timeout. A desconexão sinaliza cancelamento para impedir etapas posteriores. `/api/health` é independente da inferência e `/api/status` valida o acervo e os modelos.

Snapshots atuais incluem código, prompts, configuração, versões instaladas e metadados/vetores do índice quando disponível. A ferramenta de expiração atua somente sobre logs comuns novos; registros históricos e sintéticos são preservados. A verificação adicional usa o mesmo modelo e não substitui julgamento humano. O piloto histórico não foi executado novamente nem usado como avaliação da versão revisada.
