# Prova de conceito com guardrails — entrega revisada de Projeto/TCC I

Autor: Filipe Martins Henrique. Orientador informado no projeto: Prof. Marcos Souza. Revisão de 03/11/2026.

## Comece aqui

1. Leia o PDF em `output/pdf/TCC_PoC_TCCI_revisado.pdf`.
2. Para editar, use `main.tex` e `texto/`, ou importe `Overleaf_TCC_PoC.zip` com XeLaTeX. As instruções estão em `LEIA-ME_OVERLEAF.md`.
3. Confira `avaliacao/MATRIZ_PARECER.md` e `ALTERACOES_E_PENDENCIAS.md` para localizar as correções e as dependências externas.
4. Para avaliação posterior, leia `avaliacao/PROTOCOLO.md` e `RUBRICA.md`. As duas planilhas estão em `outputs/guardkids_revisao_20261103/`: instrumento completo e cópia com condições omitidas. A chave está separada em `avaliacao/chave_decodificacao.csv`.

O pacote inclui código, casos, respostas fictícias de desenvolvimento, snapshots, congelamentos e evidências de testes. O arquivo `MANIFESTO_SHA256.json`, dentro do ZIP completo, permite conferir integridade.

## O que foi verificado

- 45 testes em Python e um teste JavaScript aprovados, com XML/TAP preservados.
- Dois lotes novos de 54 execuções cada, sobre as mesmas 27 perguntas fictícias de desenvolvimento. Não são 108 perguntas independentes.
- Sondagem de três limiares apenas no desenvolvimento.
- PDF compilado, com inspeção visual; pacote Overleaf compilado localmente em pasta isolada. Não houve edição remota no serviço.
- Planilhas recalculadas, inspecionadas e verificadas após importação com simulação de cálculo em memória. Não foi aberto o Microsoft Excel; nenhum dado simulado de julgamento foi salvo nos instrumentos.

## O que continua pendente

Ratificação humana das referências e revisão especializada do corpus; confirmação do orçamento de avaliadores; 160 julgamentos primários e 32 secundários após as execuções finais; orientação/formalização institucional e conferência de direitos de reutilização antes de publicação. A avaliação final não foi executada e não se afirma segurança geral ou eficácia educativa.

O protótipo ainda apresentou falhas de classificação e sustentação no desenvolvimento, discutidas no capítulo de evidências. A correção do campo de ajuda não é apresentada como solução universal.

Os PDFs didáticos completos, pesos de modelos, ambientes e credenciais não integram este pacote. Para inferência, obtenha as fontes originais compatíveis com seus hashes e modelos locais indicados no protocolo. Para compilar o texto não é necessário executar a inferência.

As alterações foram salvas localmente, sem commit, push, publicação ou envio a terceiros. O backup dos originais está preservado na pasta `historico/` do workspace; não é necessário para usar os arquivos revisados deste pacote.
