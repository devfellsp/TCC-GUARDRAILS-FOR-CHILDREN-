# GK-P2.5-dev — revisão das respostas e verificadores

Esta é a revisão de desenvolvimento recomendada após as correções. Mantém os 18 blocos da GK-P2.2-dev, sem acrescentar fontes para justificar saídas anteriores. As versões GK-P2.1-dev (TCC), GK-P2.2-dev (ampliação inicial) e seus resultados permanecem preservados. As GK-P2.3-dev e GK-P2.4-dev conservam as rodadas intermediárias e seus diagnósticos; não são as versões recomendadas.

## Abrir e selecionar

Com Ollama disponível e os mesmos modelos locais instalados, execute na raiz:

```powershell
poc/versions/GK-P2.5-dev/Iniciar_GK_P2_5.cmd
# Abrir http://127.0.0.1:8769
```

Para retornar ao sistema do TCC, encerre a interface atual e use `poc/Iniciar_GuardKids.cmd`, porta 8765. Para a ampliação inicial use `poc/versions/GK-P2.2-dev/Iniciar_GK_P2_2.cmd`, porta 8766. Use uma versão por vez para evitar disputa dos modelos. Nenhum comando original passou a selecionar automaticamente esta revisão.

O perfil continua fictício, nove anos e quarto ano; sem participantes infantis. O índice é o mesmo da ampliação, validado contra as fontes originais, com cópia preservada própria. Para restaurar somente esse índice, sem inferência, execute `poc/.venv/Scripts/python.exe -B poc/versions/GK-P2.5-dev/restore_index.py` na raiz.

## Correções

1. O estilo passo a passo deixou de exigir introdução, dois passos e exemplo em todas as respostas. Agora apresenta de uma a três afirmações, numeradas pelo programa. Uma definição simples pode ocupar uma única linha.
2. Cada afirmação identifica suas fontes. O programa obtém o texto literal diretamente dos blocos recuperados: o gerador não redigita citações, evitando trechos inventados, reticências e erros de associação de texto a ID.
3. Uma barreira lexical conservadora retém afirmações com palavras de conteúdo ou números sem âncora nas fontes citadas. Conectivos, pronomes, verbos auxiliares e flexões simples têm tratamento próprio. A regra vale para todos os temas e não contém respostas prontas aos casos testados.
4. O auditor confere cada afirmação, a precisão da resposta à pergunta e a redação. Afirmação rejeitada, falta de veredito, índice duplicado, erro de termo ou redação reprovada impedem a liberação. O texto final é montado somente a partir do candidato aprovado. Há apenas uma geração de texto por tentativa; a alternativa literal é selecionada pelo programa, sem conhecimento externo.
5. Relatos de ameaça com pedido de ajuda têm prioridade de perigo sobre humilhação. Há também uma defesa local para classificação equivocada entre essas duas categorias. A mensagem orienta procurar um adulto, buscar um lugar seguro se possível, evitar confronto e pedir ajuda imediata se houver perigo atual. Pedidos para produzir ameaças continuam bloqueados.
6. Os rótulos e exemplos dos chats agora incluem os temas do acervo ampliado. Os logs comuns omitem também os novos rascunhos, textos de evidência e justificativas individuais; logs integrais continuam exclusivos de dados declaradamente fictícios.

## Limites da revisão

A barreira lexical não prova implicação lógica. Prefixos comuns podem corresponder a sentidos diferentes, palavras curtas não recebem o mesmo filtro e uma afirmação pode usar palavras da fonte e ainda mudar seu significado. Por isso a verificação semântica e a revisão humana continuam necessárias. O auditor usa o mesmo modelo do gerador, em uma chamada separada; não é uma avaliação independente.

O controle é conservador e pode reter paráfrases corretas, inclusive sinônimos sem correspondência lexical. O sistema prefere informar que não concluiu uma resposta apoiada a acrescentar detalhes. As abstenções e seus motivos ficam registrados. Quando a reformulação falha na ancoragem ou na auditoria, há uma única alternativa automática: até três sentenças literais do primeiro bloco recuperado, limitadas a 120 palavras. Essa alternativa passa pela auditoria de pertinência à pergunta, redação e proteção de saída. Ela pode ser recusada; o texto da fonte não é liberado só por existir. A interface identifica o resultado como “Trecho do material”. Não há nova geração, repetição seletiva de tentativas ou substituição do rascunho rejeitado: os dois candidatos e seus motivos permanecem registrados. Se a saída acionar proteção, não se tenta a alternativa para contornar a decisão.

A avaliação final reservada não foi executada nem ajustada. O protocolo existente pertence à GK-P2.1-dev. Qualquer uso futuro desta revisão no TCC exige decisão explícita e identificação de novo protocolo e congelamento. Os denominadores das versões não devem ser somados.

## Evidências e conferência

Consulte `RELATORIO_CORRECOES.md` para resultados e limites efetivamente observados. O plano e os registros desta revisão ficam em `avaliacao/evidencias/correcoes_GK_P2_5_dev_20261105/`. Os testes diagnósticos de respostas antigas ficam no subdiretório `guard_checks/`; são regressões conhecidas, sem caráter de avaliação cega.

Para conferir a versão, os arquivos antigos e os registros sem inferência:

```powershell
poc/.venv/Scripts/python.exe -B poc/versions/verificar_correcao.py
poc/.venv/Scripts/python.exe -B poc/versions/verificar_preservacao.py
poc/.venv/Scripts/python.exe -B poc/versions/verificar_ampliacao.py
```

Os comandos de lote `run_expansion.py plan/run` e `run_guard_regressions.py plan/run` recusam repetir pastas já executadas. Não os use para tentar substituir resultados existentes.

## Prazo de execução local

O prazo total é de 600 segundos, com espera de 610 segundos na interface. Em execução pela CPU, a geração e as verificações podem ultrapassar os dois minutos do limite anterior. O prazo não altera as regras de liberação da resposta; tentativas que excedem o limite continuam sendo retidas e registradas como falha técnica. Recarregue a página após atualizar o prazo da interface.
