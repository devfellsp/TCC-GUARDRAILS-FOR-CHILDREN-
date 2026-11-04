# Revisão do GuardKids: código, segurança e consistência acadêmica

**Registro histórico da auditoria inicial. As correções posteriores estão em [CORRECOES_2026-11-03.md](../CORRECOES_2026-11-03.md). Os caminhos de linha deste relatório se referem à versão auditada.**

Data: 03/11/2026. Base revisada: commit `0aa64d3` da branch `main`.

## Resultado

As prioridades são corrigir a apresentação das evidências no TCC, atualizar a dependência de leitura de PDFs e melhorar a privacidade dos registros. A implementação tem salvaguardas úteis, mas os testes atuais e o pequeno piloto não sustentam todas as garantias descritas no texto e nos diagramas.

Esta revisão não modificou o código do aplicativo, os textos acadêmicos, as dependências ou os dados do experimento. Foram acrescentados somente este relatório, um verificador isolado e arquivos de evidências nesta pasta.

P1 significa correção prioritária antes de apresentar resultados acadêmicos; P2 significa correção de segurança, confiabilidade ou reprodutibilidade; P3 significa melhoria de menor impacto. A prioridade considera a prova de conceito local com perguntas fictícias, sem participantes infantis.

## Verificações realizadas e limites

- Leitura do código Python, API, interface, scripts de início/fim, configurações, prompts, testes, documentação e textos LaTeX.
- Oito testes existentes passaram, com um aviso de descontinuação de `httpx` no cliente de testes. A restrição inicial à comunicação local do ambiente foi contornada para executar a suíte; não era uma falha do projeto.
- `pip check`: nenhuma incompatibilidade declarada entre os pacotes instalados.
- Consulta à API OSV para os 25 pacotes fixados em `requirements-lock.txt`: sete avisos para `pypdf==6.21.2`; nenhuma correspondência para os outros 24 pacotes nessa consulta. Isso não certifica ausência de vulnerabilidades desconhecidas, nem cobre o Ollama, os modelos, o Python e o sistema operacional.
- Extração das cinco passagens reais pelo código do projeto e comparação com as alegações do TCC. Conferência pontual dos artigos de Wang e Rath e do tamanho do MinorBench.
- Comparação do CSV local do piloto com as respostas apresentadas como literais no TCC. Esse CSV existe nesta máquina, mas é ignorado pelo Git.
- Verificações adicionais com dados fictícios, objetos simulados e arquivos temporários. Não foram usados PDFs maliciosos nem testes de carga.
- O serviço Ollama não estava acessível em `127.0.0.1:11434`, inclusive na conferência fora da restrição inicial. Não foi executada nova inferência: esta revisão não demonstra um jailbreak real do Qwen3 nem mede eficácia dos guardrails.
- Não havia compilador LaTeX disponível no caminho de execução. A compilação, paginação e aparência final do TCC não foram validadas. Não foram encontradas referências internas LaTeX ausentes ou rótulos duplicados na conferência estática.
- Os dois `.tex` são idênticos. As cópias no pacote Overleaf também são equivalentes ao conteúdo atual, desconsiderando finais de linha. O ZIP não foi apontado como desatualizado.

## Achados prioritários

### 1. [P1] A análise de alucinação do caso dev01 contradiz a própria fonte

**Local:** [main.tex, linha 798](C:/Users/Filipe/Documents/TCC/main.tex:798), discussão na linha 810 e as mesmas linhas de `document.tex`.

O TCC afirma que criar açúcar e ocorrer nas folhas são complementações da memória paramétrica, ausentes de `sp2024-p9-1`. A passagem efetivamente extraída dessa página contém tanto a transformação em açúcar quanto o transporte de água para as folhas, a absorção de gás carbônico e a captação de luz. `sp2024-p8-1` também menciona açúcares.

**Impacto:** o exemplo não demonstra a falha de ancoragem que a discussão lhe atribui. A premissa geral de que RAG pode falhar continua válida, mas sua demonstração empírica neste caso está incorreta.

**Recomendação:** conferir as afirmações contra todos os trechos fornecidos ao gerador; retirar essa atribuição causal de dev01. Se houver outro caso realmente não sustentado, apresentá-lo com `run_id`, trechos recuperados e justificativa. Não substituir a evidência por uma resposta reconstituída.

**Evidência:** `evidencias.json`, campo `auditoria_dev01`; reprodução pela extração real em `verificar.py`. Fonte local: `Livros_Didadicos/CadEstud_4ano_2_Bimestre_WEB.pdf`, página PDF 11 / impressa 9.

### 2. [P1] As três respostas chamadas de literais não coincidem com o CSV do piloto citado

**Local:** [main.tex, linha 785](C:/Users/Filipe/Documents/TCC/main.tex:785) e linhas 798–802; também em `document.tex`.

Os textos dos casos dev01, dev02 e dev03 da política ajustada foram comparados com `poc/runs/development_20261025_101938.csv`. Nenhum dos três coincide integralmente com a resposta registrada. Exemplos: dev01 omite a oração final sobre a captação da luz; dev02 foi reformulado; dev03 troca a formulação da última oração. Não é apenas diferença de aspas ou formatação LaTeX.

**Impacto:** prejudica a rastreabilidade e altera o material sobre o qual a rubrica é aplicada. Não se pode afirmar que o texto transcrito é a saída literal daquela rodada.

**Recomendação:** gerar a tabela diretamente dos registros, preservando o texto e vinculando cada linha a `case_id`, política e `run_id`. Se a fonte for outra rodada, identificá-la explicitamente. Separar transcrição de paráfrase.

**Evidência:** `evidencias.json`, campo `piloto_local`; comparação com o CSV local ignorado pelo Git. A presença de uma versão diferente em outra rodada não foi descartada, mas não justificaria atribuí-la ao CSV indicado.

### 3. [P1] Métricas de conteúdo e tempos têm sustentação documental insuficiente ou contraditória

**Local:** [main.tex, linha 737](C:/Users/Filipe/Documents/TCC/main.tex:737), linhas 779 e 822; [registro de execução, linha 28](C:/Users/Filipe/Documents/TCC/poc/docs/REGISTRO_DE_EXECUCAO.md:28).

O TCC apresenta `T_RI=0/11`, tratamento adequado de `7/7` riscos e eficácia de 100%. Entretanto, as 22 linhas do CSV local estão sem preenchimento dos campos de julgamento humano, e a documentação técnica registra expressamente que concordância das rotas não mede adequação do conteúdo. Uma avaliação humana pode ter sido feita em outro documento, mas não está vinculada aos registros apresentados.

Além disso, o TCC associa os 79,16 segundos de carga a frio à primeira das 22 execuções e fala em 21 execuções subsequentes. O registro técnico diz que os aproximadamente 79 segundos pertencem a uma rodada anterior; todas as 22 linhas do CSV citado têm duração de até 5,845 segundos.

**Impacto:** decisões automáticas podem estar sendo apresentadas como avaliação de segurança, e a população usada para as estatísticas de latência fica ambígua.

**Recomendação:** manter as contagens de rotas como resultado funcional; calcular métricas substantivas somente com julgamentos documentados. Identificar o registro da carga a frio separadamente. Limitar conclusões aos casos de calibração, sem inferir generalização. Registrar a rubrica, justificativa, avaliador e data para cada resposta.

### 4. [P2] A versão instalada de pypdf possui sete avisos de segurança conhecidos

**Local:** [requirements-lock.txt, linha 20](C:/Users/Filipe/Documents/TCC/poc/requirements-lock.txt:20); uso em [guardkids.py, linha 145](C:/Users/Filipe/Documents/TCC/poc/guardkids.py:145).

`pypdf==6.21.2`, confirmado no ambiente instalado, corresponde a sete avisos retornados pela OSV:

| Aviso | Operação afetada | Primeira correção informada |
|---|---|---|
| GHSA-5849-834g-hvw5 / CVE-2026-119203 | Abertura de PDF incompleto sem trailer: loop infinito | 6.21.4 |
| GHSA-cggf-277g-3q54 / CVE-2026-119204 | Análise da árvore de páginas: memória excessiva | 6.21.4 |
| GHSA-mfr5-77xh-9j7h / CVE-2026-119205 | Clonagem de dicionários: loop infinito | 6.21.4 |
| GHSA-42gh-23hr-vphw / CVE-2026-119206 | Leitura de rótulos de página: tempo excessivo | 6.21.3 |
| GHSA-4vqv-7265-gm2w / CVE-2026-119207 | Erros em modo estrito: memória excessiva | 6.21.3 |
| GHSA-62m5-6wh8-28x7 / CVE-2026-119208 | Contagem de páginas de PDF criptografado | 6.21.3 |
| GHSA-x3rh-gjgm-fmqc / CVE-2026-119209 | Abertura de fluxos de referência cruzada: memória excessiva | 6.21.3 |

Os caminhos de abertura e leitura de páginas são relevantes à extração do corpus. Clonagem, leitura de rótulos e modo estrito não são usados explicitamente pelo extrator atual; não se deve tratar os sete avisos como sete explorações demonstradas no aplicativo.

**Impacto:** PDF malformado pode travar a indexação ou consumir memória. A interface não oferece upload e o manifesto usa arquivos locais selecionados, limitando a exposição atual. Nenhum PDF do repositório foi demonstrado malicioso.

**Recomendação:** atualizar para uma versão revisada que inclua as correções de `6.21.4`, regenerar o lock e repetir a extração e seus testes. Caso a aplicação passe a receber PDFs de terceiros, executar a extração em processo com limite de tempo e memória.

Fontes primárias: [aviso de loop na abertura](https://github.com/py-pdf/pypdf/security/advisories/GHSA-5849-834g-hvw5), [aviso de memória na árvore de páginas](https://github.com/py-pdf/pypdf/security/advisories/GHSA-cggf-277g-3q54), [versão 6.21.4](https://github.com/py-pdf/pypdf/releases/tag/6.21.4). Respostas completas da consulta estão em `dependencias_e_ambiente.json` e `avisos_pypdf.json`.

## Privacidade, integridade e funcionamento

### 5. [P2] A orientação de privacidade não impede a gravação do dado recebido

**Local:** [guardkids.py, linha 237](C:/Users/Filipe/Documents/TCC/poc/guardkids.py:237) e linha 277; promessa de interceptação antes do processamento em `main.tex`, linha 319; regex alegada no guia de diagramas, linha 72.

A pergunta integral é enviada ao classificador e gravada em texto, mesmo quando a ação é `safe_guidance` por privacidade. Também ficam nos registros rascunhos rejeitados. Não há mascaramento prévio ou regra determinística de privacidade no código atual. A regex existente serve à limpeza e à fragmentação de texto.

**Impacto:** alguém que informe dados reais apesar do aviso terá esses dados persistidos. O comportamento é parcialmente explicado no LEIA-ME e aceitável apenas dentro do escopo controlado de perguntas fictícias; não comprova exposição remota nem participação real de crianças.

**Recomendação:** separar o modo de pesquisa com dados sintéticos de qualquer modo de uso real. Definir retenção, acesso e exclusão dos registros; minimizar ou mascarar identificadores antes de persistir dados reais. Uma regex pode complementar a proteção, mas não garante detectar todos os identificadores. Corrigir as afirmações de que o protótipo impede o processamento ou a coleta por si só.

**Reprodução:** pergunta contendo apenas um contato fictício `.invalid`, classificador simulado com privacidade e inspeção do arquivo temporário: pergunta integral preservada.

### 6. [P2] Texto e metadados dos trechos podem divergir dos vetores sem detecção

**Local:** [guardkids.py, linha 184](C:/Users/Filipe/Documents/TCC/poc/guardkids.py:184), especialmente linhas 195–201.

O código confere manifesto, PDFs, modelo, hash dos vetores e quantidade de trechos. Porém, uma alteração somente no texto, ID ou página de um trecho em `chunks.json` não é comparada com um valor confiável da versão construída. O hash retornado por `digest(meta)` registra a nova versão, mas não rejeita essa divergência.

**Impacto:** edição acidental ou local maliciosa pode fazer a busca recuperar texto que não corresponde ao vetor e atribuí-lo à fonte original. Exige acesso de escrita local ao arquivo; nenhum caminho de escrita via HTTP foi identificado. É sobretudo um problema de consistência e rastreabilidade da base.

**Recomendação:** vincular vetores, textos e metadados em um artefato versionado e validá-lo contra um identificador congelado fora do arquivo mutável. Para resistência a adulteração, o identificador precisa estar em local protegido. Um hash recalculável ao lado do conteúdo não protege contra quem pode editar ambos. Gravar a nova versão do índice de forma atômica.

**Reprodução:** alteração só do texto em um índice fictício; a recuperação continuou aceitando o trecho, com vetores e PDF inalterados.

### 7. [P2] O serviço pode declarar prontidão com índice quebrado

**Local:** [app.py, linha 27](C:/Users/Filipe/Documents/TCC/poc/app.py:27).

`/api/status` verifica somente a existência de `index.npz` e os nomes dos modelos. Não verifica se o NPZ abre, se `chunks.json` existe, se os hashes e dimensões conferem, ou se o índice corresponde aos modelos atuais.

**Impacto:** a interface mostra o acervo como disponível e as perguntas falham com erro técnico. O teste isolado obteve `ready=true` com NPZ inválido e metadados ausentes.

**Recomendação:** validar o índice no início e manter um estado de prontidão com causa de falha; invalidar esse estado quando mudar a versão do corpus ou modelo. Separar disponibilidade do processo de prontidão do fluxo completo.

### 8. [P2] Requisições ficam em fila sem limite de espera

**Local:** [guardkids.py, linha 225](C:/Users/Filipe/Documents/TCC/poc/guardkids.py:225), cliente HTTP na linha 77 e rota síncrona em `app.py`, linha 34.

O `threading.Lock` serializa todo o processamento, sem prazo para adquirir o bloqueio. Cada chamada de rede permite até 240 segundos de inatividade segundo os limites do cliente; isso não é um prazo global da interação. Não há rejeição explícita de excesso de trabalhos pendentes ou cancelamento associado à saída do usuário.

**Impacto:** vários clientes locais podem ocupar os trabalhadores enquanto aguardam o modelo, atrasando inclusive outras rotas síncronas. O botão desabilitado limita apenas uma interface. Trata-se de risco de disponibilidade identificado por leitura do fluxo; não foi feito teste de carga ou ataque de negação de serviço.

**Recomendação:** limitar a fila, retornar ocupação controlada (`429`/`503`), definir prazo total e tornar a espera cancelável. Manter a consulta de prontidão independente de inferência demorada.

### 9. [P2] O snapshot não arquiva todos os elementos necessários à reprodução

**Local:** [guardkids.py, linha 208](C:/Users/Filipe/Documents/TCC/poc/guardkids.py:208) e `main.tex`, linha 602.

O snapshot inclui configuração, manifesto, prompts, conteúdo de `guardkids.py` e texto do lock. Não inclui os vetores, textos do índice, outros módulos e executor, versão do Ollama ou verificação das versões efetivamente instaladas. Os registros individuais guardam informações adicionais, mas índice e execuções ficam fora do Git. O texto acadêmico descreve um snapshot do índice e arquivo `runs.jsonl`, que não correspondem à implementação.

**Impacto:** os hashes permitem identificar parte de uma execução, mas não restauram os artefatos ausentes. Outra pessoa que clonar o projeto não recebe as evidências completas das tabelas.

**Recomendação:** exportar um pacote de experimento com commit, índice congelado, modelos identificados por digest, versões reais, configuração, entradas, resultados e julgamentos sintéticos. Documentar separadamente materiais cuja redistribuição não esteja esclarecida. Manter registros contendo dados reais fora da publicação.

## Divergências documentais e qualidade

### 10. [P2] Diagramas e descrição dos testes atribuem capacidades inexistentes ao projeto

**Locais:** [guia de diagramas, linha 72](C:/Users/Filipe/Documents/TCC/diagramas/GUIA_DOS_DIAGRAMAS_E_EXPLICACOES.md:72), linhas 81 e 90; [main.tex, linha 731](C:/Users/Filipe/Documents/TCC/main.tex:731).

O guia e os SVG/Draw.io citam `poc/guardkids_core/pipeline.py`, `rag.py`, `evaluate_guardrail_policy`, `final_status`, `out_of_scope`, `rejected_response` e logs JSONL. O código real usa `poc/guardkids.py`, `decision`, `action`, `redirect`, `generated` e um JSON por execução. O diagrama converte citação inválida em falta de escopo, enquanto o código registra erro técnico. A árvore do guia ainda permite `category=normal` antes de verificar `needs_protection`; a função real dá precedência ao sinal de proteção, independentemente da categoria.

A enumeração de oito testes no TCC também não corresponde à suíte versionada: não há teste de extração e integridade do corpus, resposta educativa final permitida completa ou `supported=false`. Há outros testes reais omitidos da lista, incluindo o filtro da resposta HTTP. Não é correto afirmar que esses caminhos ausentes foram cobertos pela suíte apresentada.

**Recomendação:** alinhar o texto, o gerador dos diagramas e seus arquivos gerados ao código real; distinguir arquitetura proposta e implementada. Referenciar os testes pelos nomes existentes e acrescentar cobertura de extração, recuperação, falhas de integridade e sucesso ponta a ponta com dependências controladas.

### 11. [P3] A fragmentação não respeita um limite rígido de caracteres

**Local:** [guardkids.py, linha 125](C:/Users/Filipe/Documents/TCC/poc/guardkids.py:125).

Uma sentença maior que `chunk_chars` é inserida inteira. Ao manter a sentença anterior como sobreposição, o algoritmo também pode criar um novo bloco acima do alvo sem nova divisão. O teste com alvo 850 produziu blocos de 901 e 1.803 caracteres.

**Impacto:** na ampliação do corpus, blocos grandes podem prejudicar o orçamento de contexto e a recuperação. Os cinco trechos atuais têm entre 470 e 746 caracteres, portanto esse problema não invalida o índice atual. O LEIA-ME técnico fala em alvo, mas o TCC descreve um máximo.

**Recomendação:** definir se o valor é alvo ou limite; para limite rígido, tratar sentenças longas e limitar a sobreposição. Preferir orçamento por tokens quando o corpus crescer.

### 12. [P3] Há uma leitura cumulativa incorreta de uma estatística bibliográfica

**Local:** [main.tex, linha 330](C:/Users/Filipe/Documents/TCC/main.tex:330), também em `document.tex`.

O texto diz que 48,12% das falhas ocorreram até o terceiro turno. Na seção 5.4 e Tabela 6 de Rath et al., página PDF 6, o valor é a parcela do terceiro turno na distribuição do primeiro turno prejudicial. As parcelas do primeiro, segundo e terceiro turnos são 25,25%, 2,99% e 48,12%; a soma até o terceiro é 76,36%.

**Recomendação:** escrever no terceiro turno para 48,12%, ou informar o acumulado com seu cálculo e denominador. Os valores de 64% e 85% de Wang foram localizados nas páginas PDF 12 e 9, respectivamente; o segundo se refere aos trabalhos sobre tutores/intervenções personalizados analisados pelo artigo, não a todo tutor disponível.

## Melhorias recomendadas sem exploração confirmada

- **Restringir hosts da API.** Um POST com `Host` e `Origin` arbitrários recebeu 200 no cliente de testes. O aplicativo não verifica hosts ou origem e não exige token local. Isso é uma lacuna de defesa para cenários como DNS rebinding; não foi demonstrada exploração por navegador. O bind em `127.0.0.1` continua limitando acesso direto da rede. O FastAPI instalado rejeitou JSON sem `Content-Type` e com `text/plain` (422), e não houve liberação de CORS: não foi confirmada a via simples de CSRF sem cabeçalho JSON. Adotar hosts locais explícitos e proteção de origem/requisição proporcional ao modo de uso. A [documentação do Starlette](https://starlette.dev/middleware/) explica a validação de host; a [documentação do FastAPI](https://fastapi.tiangolo.com/advanced/strict-content-type/) descreve a proteção por tipo de conteúdo.
- **Separar identidade de citação e sustentação semântica.** `source_ids` válidos não provam uma resposta verdadeira ou apoiada na fonte. A simulação liberou uma afirmação falsa com ID válido quando os classificadores de segurança também a permitiram. Isso demonstra ausência dessa verificação no orquestrador, sem provar que o modelo real geraria ou liberaria aquela frase. Revisar apoio por afirmação, avaliar recuperação e ancoragem separadamente e manter julgamento humano independente.
- **Ampliar testes adversariais.** Só há um caso simples de injeção no piloto. Acrescentar paráfrases, erros ortográficos, Unicode, pedidos compostos, contexto de citação, injeção indireta em fonte controlada e pares com e sem intenção de dano. Usar desenvolvimento separado da avaliação e não ajustar regras após observar os resultados finais. RAG e prompts não eliminam injeção, conforme a [OWASP](https://genai.owasp.org/llmrisk/llm01-prompt-injection/). O mesmo Qwen3 como gerador e classificador é uma limitação já reconhecida no LEIA-ME; comparar uma verificação independente é uma evolução possível, não uma garantia automática.
- **Concluir o protocolo experimental.** Fixar quantidade de casos por categoria, versões, ordem das execuções, repetições e tratamento de pares com falha técnica. Distinguir taxa em solicitações de risco e taxa global para não diluir falhas em muitas perguntas benignas. Uma referência que bloqueia explicitamente toda predação é uma ablação útil desse parâmetro, mas não representa, sozinha, comparação com a melhor alternativa disponível.
- **Centralizar a versão principal do TCC.** `main.tex` e `document.tex` são cópias integrais iguais; o README ainda descreve o documento como metodologia pendente de atualização. Manter uma fonte e um processo de empacotamento para reduzir divergências futuras.
- **Limpar a interface antes de cada tentativa.** Em `poc/web/index.html`, linha 15, o tratamento de erro muda a resposta e reexibe o cartão sem limpar fontes, metadados, etapas e identificador da pergunta anterior. Uma falha HTTP após um sucesso pode associar dados antigos à nova tentativa. Limpar esses campos e apresentar estado de erro próprio.
- **Validar configuração e escrita de registros.** Tipar políticas/configuração, evitar padrões duplicados entre CLI/API/config e tratar falha de gravação explicitamente. A escrita do log está fora do `try` principal; falha de disco pode resultar em 500 sem o registro esperado. Se uma execução só é válida quando auditável, sua finalização deve incluir persistência bem-sucedida.
- **Documentar reutilização dos materiais.** Corpus, PDFs científicos, livros e datasets têm condições próprias. A pendência já está reconhecida no projeto. Conferir licenças, origem e créditos antes de ampliar redistribuição; esta revisão não conclui situação jurídica desses arquivos.
- **Automatizar verificações.** Executar testes, verificação de dependências e construção do texto em integração contínua. O aviso atual de descontinuação do cliente de testes não causa falha, mas precisa de migração planejada.

## O que já está adequado

- O serviço é iniciado por padrão somente no endereço local.
- O navegador recebe campos selecionados da resposta; o teste existente confirma que rascunho rejeitado e texto recuperado não são expostos pela API.
- A interface usa `textContent` para respostas e fontes; não foi identificado um caminho direto de execução de HTML gerado pelo modelo.
- Esquemas do gerador e classificador usam tipos estritos e rejeitam campos extras.
- Falhas do modelo são convertidas em perda técnica e não em proteção bem-sucedida.
- A decisão de proteção precede a exceção de predação na função real.
- A leitura do NPZ não habilita carregamento de objetos por pickle.
- A documentação técnica reconhece limites de corpus, julgamento pelo mesmo modelo, ausência de participantes infantis e contaminação do piloto por calibração.

## Ordem sugerida de execução

1. Corrigir os achados 1–3 e 10 no texto e nas evidências antes de apresentar resultados à banca.
2. Atualizar pypdf e validar que a extração seleciona exatamente os mesmos trechos.
3. Definir e implementar o tratamento de registros de privacidade conforme o modo de uso.
4. Corrigir integridade do índice, prontidão, limite de fila e pacote reprodutível do experimento.
5. Congelar o protocolo e executar avaliação independente com julgamentos documentados.

## Como repetir as verificações

Na raiz do projeto, com o ambiente existente:

```powershell
.\poc\.venv\Scripts\python.exe -m pytest poc/tests -q
.\poc\.venv\Scripts\python.exe poc/docs/revisao_2026-11-03/verificar.py
```

O segundo comando não chama modelos reais. Ele cria arquivos em uma pasta temporária sob `.cache`, remove esses arquivos ao terminar e regrava `evidencias.json` com os resultados. O cliente de testes precisa de comunicação local permitida no Windows. Em outro clone, a comparação do CSV fica indicada como indisponível se os registros locais não estiverem presentes.

Os arquivos de consulta OSV representam a situação consultada nesta revisão; novas consultas podem retornar resultados diferentes. Não houve commit, envio ao GitHub ou aplicação de correções neste trabalho.

