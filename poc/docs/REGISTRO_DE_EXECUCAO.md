# Registro da instalação e verificação — 25/10/2026

## O que foi executado

- Conferência do Anaconda, Ollama, memória RAM de aproximadamente 16 GB e RTX 4060 com 8 GB de VRAM.
- Ambiente isolado Python 3.12 em `poc/.venv`; ambiente base preservado.
- Instalação de FastAPI, Uvicorn, pypdf, NumPy, HTTPX, pytest e dependências. Versões em `requirements-lock.txt`.
- Download oficial de Qwen3 8B Q4_K_M (aproximadamente 5,2 GB) e BGE-M3 (aproximadamente 1,2 GB) pelo Ollama.
- Extração de cinco passagens das duas apostilas, com fontes, páginas e hashes; vetores normalizados de 1024 dimensões.
- Construção do fluxo de classificação de entrada, busca, geração com fontes, verificação de saída e registro.
- Interface e serviço local em `http://127.0.0.1:8765`, sem exposição à rede local.
- Oito testes de lógica e integração interna passaram. Um aviso de descontinuação da dependência de teste HTTPX foi emitido, sem falha.
- Verificação real da API: serviço pronto, resposta educativa com fontes e bloqueio de solicitação para ferir animal.
- Sintaxe do JavaScript da interface validada. A abertura no navegador foi recusada pela política de acesso; a interface não recebeu inspeção visual nesta sessão.
- Quatro diagramas editáveis e explicações salvos em `docs/ARQUITETURA_E_DECISOES.md`.
- Atualização do README e preservação do texto acadêmico para revisão posterior; não foram inseridos resultados experimentais finais no capítulo.

## Desenvolvimento e correções

A primeira rodada confundiu dano a animais com autolesão; uma rodada ampliada confundiu ocultação de consumo de álcool com autolesão. As instruções foram esclarecidas e os registros anteriores preservados. Essas correções foram feitas sobre perguntas de desenvolvimento. Nenhum desses casos deve migrar para a avaliação final como pergunta inédita.

## Última rodada do piloto

- CSV: `runs/development_20261025_101938.csv`.
- 22 execuções: 11 perguntas em duas configurações.
- 22 execuções válidas; 0 perdas técnicas.
- 0 divergências entre rotas observadas e as rotas esperadas do pequeno conjunto de desenvolvimento.
- Duração com modelo carregado: mínimo 0.89 s, mediana 1.09 s, máximo 5.84 s.
- A primeira carga do modelo em rodada anterior levou aproximadamente 79 s; não está incluída nesses tempos.
- Os julgamentos humanos de conteúdo inadequado, bloqueio indevido e qualidade permanecem vazios no CSV.

## Limites e próximo passo

O piloto demonstra execução dos caminhos escolhidos e registro das decisões. Não é medição de eficácia: as mesmas perguntas ajudaram a calibrar as instruções, e o verificador usa o mesmo modelo do gerador. Corpus, regras, prompts e amostra precisam ser revisados e congelados antes da avaliação final. As condições de reutilização dos livros e seus créditos de terceiros ainda precisam de documentação para publicação.

Próximo passo: revisar com o pesquisador as respostas e decisões do piloto, finalizar a seleção do corpus e a política, converter os diagramas para figuras acadêmicas e atualizar o capítulo de metodologia. A revisão bibliográfica ainda não foi redigida nesta etapa.
