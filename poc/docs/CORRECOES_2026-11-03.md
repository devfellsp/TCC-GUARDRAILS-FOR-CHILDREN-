# Correções do GuardKids — 03/11/2026

As correções foram aplicadas sobre a versão `0aa64d3`. A auditoria original permanece em `revisao_2026-11-03/RELATORIO.md` como registro histórico. Os dados antigos de pesquisa foram preservados. As mudanças de comportamento não foram aplicadas retroativamente às respostas do piloto.

## Correspondência com os 12 achados

| Achado | Correção aplicada |
|---|---|
| 1. Análise incorreta de dev01 | Removida a atribuição de açúcar e folhas à memória paramétrica; o texto reconhece essas informações nas fontes. |
| 2. Transcrições diferentes dos registros | Conferidas 22 execuções fictícias contra casos e registros locais; evidências em `pilot_evidence.json`. A tabela literal é gerada automaticamente com fontes e identificadores completos. |
| 3. Métricas sem julgamento e carga a frio | Retiradas as taxas de conteúdo derivadas apenas de ações; rubrica marcada como pendente. A carga inicial é identificada como rodada anterior às 22 execuções medidas. |
| 4. pypdf vulnerável | Ambiente e lock atualizados para 6.21.4. Extração real dos cinco trechos testada; nova consulta OSV sem correspondências para os 28 pacotes fixados. |
| 5. Privacidade dos registros | Texto livre omitido dos novos logs comuns. Alguns identificadores explícitos são detectados antes do modelo. Conteúdo completo somente em execução declarada fictícia por CLI/executor; esse parâmetro não é aceito pela API. |
| 6. Integridade dos trechos | Índice validado contra extração dos PDFs, com normalização de espaços, manifesto, metadados, hashes, dimensões, finitude e norma dos vetores. Versões completas publicadas antes da troca atômica do ponteiro ativo. |
| 7. Prontidão incorreta | `/api/status` valida modelos e índice; falha de configuração/acervo resulta em `ready=false`. `/api/health` informa apenas vida do processo. |
| 8. Fila sem limite | Uma execução por vez, com recusa imediata das demais (429); orçamento de inferência e sinal de cancelamento. Leitura de rede em andamento termina ao responder ou atingir seu timeout. |
| 9. Snapshot incompleto | Incluídos módulos, prompts, configuração, versões reais, Python/plataforma, commit e metadados/vetores do índice quando disponível. Exportação permite apenas registros explicitamente fictícios com snapshot validado. |
| 10. Documentação e diagramas divergentes | Corrigidos caminhos, campos, ações e precedência das decisões; diagramas regenerados. A enumeração dos oito testes históricos corresponde à suíte original, e a suíte atual cobre os novos controles. |
| 11. Fragmentação acima do limite | Sentenças longas são subdivididas; sobreposição é reduzida para cumprir o limite rígido. |
| 12. Estatística bibliográfica | Corrigido “até o terceiro turno” para “no terceiro turno” no valor de 48,12%. |

## Melhorias adicionais

- Configuração tipada e validada; endpoint do modelo limitado a HTTP local.
- API com validação de hosts/origens e limite de 8 KiB antes de interpretar JSON; corpo e políticas tipados, campos extras recusados.
- Verificação adicional de sustentação por outra chamada ao Qwen3, além da validação dos IDs. Ela compartilha limitações com o gerador e não equivale a avaliação independente.
- Limite de 120 palavras aplicado pelo código.
- Gravação atômica dos registros e retenção da resposta em caso de falha (503).
- Interface limpa resposta, fontes, etapas e identificadores antes de cada tentativa e ao ocorrer erro; tempo de espera e mensagem de ocupação tratados.
- CLI comum mostra somente resposta liberada e metadados públicos, preservando a minimização do arquivo em disco.
- Expiração manual dos novos logs minimizados após o prazo configurado; prévia sem apagar arquivos por padrão. Registros legados e sintéticos ficam fora dessa limpeza.
- Suíte adicional com oito casos adversariais fictícios, separada das perguntas históricas. Esses casos são desenvolvimento, não avaliação final. Execute com `run_development.py --suite adversarial`; a ordem das políticas alterna entre casos.
- Resumo de conteúdo só calcula `T_RI` quando todas as execuções válidas da política têm julgamento, justificativa, avaliador e data.
- Uma única fonte principal (`main.tex`); `document.tex` carrega essa fonte. Tabela literal e pacote Overleaf gerados por `tools/build_assets.py`, com empacotamento determinístico.
- Corrigidos quebra de identificadores, caracteres ordinais e separação entre autor e local na capa; referências internas do PDF recebem identificadores únicos.
- Fluxo de integração contínua preparado com testes Python/JavaScript, verificação dos artefatos, auditoria de pacotes e compilação LaTeX. A execução no GitHub ocorrerá após envio das alterações; os jobs remotos não foram executados nesta sessão.

## Validação executada

1. **35 testes Python passaram**, cobrindo a suíte original e regressões de corpus, índice, privacidade, sustentação, prontidão, concorrência, prazo/cancelamento, persistência, configuração, expiração, snapshots e exportação.
2. **Um teste JavaScript passou**: após uma resposta bem-sucedida, um erro não reapresenta fontes, etapas, metadados ou ID antigos.
3. **Cinco verificações reais com modelos locais concluíram sem erro técnico**: identificador fictício → orientação segura sem chamada ao modelo; pergunta educativa → resposta com fontes e verificação adicional; pedido de dano → bloqueio; predação → bloqueio na referência e resposta na ajustada. São verificações funcionais de desenvolvimento, não medidas de eficácia. IDs, digests e tempos estão em `revisao_2026-11-03/verificacao_real.json`. O servidor Ollama foi iniciado apenas para esses testes e encerrado depois; os pesos existentes foram utilizados sem download de modelos.
4. **Dependências compatíveis** segundo `pip check`; a consulta OSV dos 28 pacotes fixados retornou zero avisos correspondentes na data da revisão. Evidência em `revisao_2026-11-03/dependencias_corrigidas.json`. Isso não certifica ausência de falhas desconhecidas nem cobre executáveis/modelos externos ao lock.
5. **Índice anterior migrado e validado** sem nova vetorização. A cópia anterior foi preservada em `poc/data/`; as novas versões geradas permanecem fora do Git.
6. **TCC compilado em PDF** com verificação de capa, tabelas e cronograma renderizados. Sem transbordos horizontais, referências indefinidas ou caracteres ausentes detectados no log final. O compilador portátil emitiu avisos de codificação em três linhas da dependência `algorithm2e`, sem caracteres de substituição no texto extraído do PDF.

## Limites que dependem das próximas etapas da pesquisa

Não foram inventados julgamentos humanos, autorizações de reutilização ou resultados de avaliação independente. Ainda é necessário revisar direitos e créditos dos materiais, concluir a calibração da versão atual, fixar amostra/repetições/ordem/critérios antes do experimento final e registrar julgamentos humanos. O perfil de nove anos e as perguntas fictícias não comprovam compreensão por crianças de sete a onze anos.

A detecção de identificadores é parcial; a proteção de persistência depende principalmente da omissão de texto livre. Logs integrais exigem declaração explícita de uso fictício, cuja responsabilidade é do pesquisador. Registros antigos não foram apagados nem anonimizados retroativamente. Os snapshots guardam trechos curriculares, não os PDFs originais ou os pesos dos modelos; os direitos desses trechos continuam relevantes para redistribuição.

Nenhuma camada automática assegura ausência de alucinação, injeção de prompt ou conteúdo inadequado. As novas verificações e a ampliação dos testes reduzem lacunas de implementação, mas não substituem a avaliação independente prevista na metodologia.
