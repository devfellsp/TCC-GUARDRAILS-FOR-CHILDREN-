# TCC GuardKids — edição GK-P2.6-dev

A revisão mais recente trata as marcações vermelhas, amarelas e os quatro comentários da introdução: `avaliacao/REVISAO_MARCACOES_INTRODUCAO_2026-11-05.md` registra cada decisão. O diagrama 1 atualizado e o foco principal aprovado foram mantidos.

O manuscrito foi realinhado à ficha do tema: a comparação principal é entre duas configurações de proteção, com indicadores de respostas inadequadas, bloqueios indevidos e tratamento de risco. A comparação de estilos é complementar. A implementação atual permanece com proteção comum; as duas condições no acervo ampliado ainda precisam ser especificadas, implementadas e avaliadas. A orientação vigente está em `avaliacao/COMPARACAO_GUARDRAILS_2026-11-05.md`; os relatos de revisões anteriores abaixo preservam seu contexto histórico.

Importe o ZIP no Overleaf, selecione main.tex e o compilador XeLaTeX. O pacote contém fontes Times New Roman, texto, sete diagramas vetoriais do Draw.io com seus originais editáveis e o cronograma em LaTeX: oito figuras ao todo.

O manuscrito apresenta a GK-P2.6-dev como artefato atual, com dez chats, seis volumes didáticos de quatro coleções, três sínteses e 40 blocos. Os resultados antigos continuam identificados por versão. As três consultas da ampliação são verificações de desenvolvimento; o plano final de 32 perguntas/64 oportunidades pertence à proposta anterior e exige replanejamento para os dez chats.

Os suplementos selecionados incluem fontes da PoC atual, manifesto, seleção de recortes, índice preservado e verificações, além dos registros históricos citados. Compilar o texto não exige executar modelos. Os PDFs didáticos completos e os modelos locais não integram este pacote; para executar a PoC, é necessário o acervo da pasta local do projeto com os hashes indicados e os modelos Qwen3:8b e BGE-M3 instalados. Registros manuais, ambiente Python e estado ativo ficam fora do pacote.

A revisão pedagógica independente e a ratificação das condições de reutilização permanecem pendentes. Os resumos usam 11 pontos, e o corpo, 12. A logo institucional foi preservada.

## Erro “fontspec requires either XeTeX or LuaTeX”

Esse erro indica que o projeto está sendo processado por pdfLaTeX/LaTeX. Mude o compilador para **XeLaTeX** nas configurações do projeto e clique em **Recompile**. O `fontspec` é necessário às fontes OpenType usadas nesta versão.

Não é necessário reenviar os arquivos para corrigir um projeto já importado. Se o log ainda indicar pdfTeX após a mudança, confirme que alterou o compilador do projeto correto e selecione **Recompile from scratch** no menu de recompilação.

O pacote inclui a indicação `% !TeX program = xelatex` nos arquivos de entrada e `latexmkrc` com XeLaTeX como padrão. Essas indicações não substituem a conferência da opção **Compiler** no Overleaf: configurações explícitas do editor podem prevalecer sobre padrões de arquivo.

Os avisos de depreciação de `babel`/`memoir` não são a causa desse erro fatal de compilador. Não é necessário modificar o texto acadêmico para resolver o problema mostrado.

Orientação conferida na [documentação oficial do Overleaf](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler).

## Notas de preparação do documento

O manual disponível no portal do curso foi consultado na revisão (UNITINS, 2025). Ajustaram-se denominação institucional, quatro palavras-chave, margens, recuo, espaçamento e apresentação. O arquivo utiliza os arquivos Times New Roman da pasta fontes/. Os resumos usam 11 pontos; o texto principal, 12 pontos. As sete figuras do Draw.io foram preservadas, com identificação acima e fonte abaixo. A compilação e a inspeção visual não constituem certificação integral de conformidade com ABNT ou com o manual.

Essas informações documentam a edição e não integram o conteúdo acadêmico do PDF. O histórico de alterações, os backups e a matriz de atendimento ao parecer ficam nos materiais de acompanhamento, fora dos capítulos e apêndices da pesquisa.

A revisão prospectiva de 04/11/2026 define o ASCS, equilibra a segunda revisão dentro de cada chat e tipo de caso e acrescenta o formulário de preferência pareada de clareza. Nenhuma resposta final ou assinatura humana foi produzida. A versão atual do PDF tem 45 páginas. O script histórico de métricas não implementa o novo protocolo.

O ASCS prospectivo possui calculador próprio em `poc/final_metrics.py`, com verificação documental e taxas condicionadas à revisão humana encerrada. Seu código acompanha o pacote; não é necessário executá-lo para compilar o manuscrito.

O cronograma usa o modelo de Gantt em `texto/cronograma.tex`, com o pacote `pgfgantt`, intervalos quinzenais e 16 atividades entre outubro/2026 e junho/2027. As barras distinguem desenvolvimento realizado de continuidade proposta. O manuscrito passa a ter oito figuras (sete Draw.io e um Gantt) e dez tabelas.

O manuscrito não contém apêndice operacional. Seu conteúdo foi transferido para `poc/docs/MATERIAIS_E_REPRODUCAO.md`, incluído no pacote como documentação de apoio.

## Materiais suplementares incluídos

Além das fontes editoriais, o ZIP inclui o lote multidisciplinar completo arquivado (agenda, resultados, revisão, 32 registros completos, snapshot, ambiente e manifesto SHA-256), os dois lotes históricos de Ciências e seus congelamentos. Os instrumentos reservados permanecem em branco. O PDF principal é entregue separadamente e não integra o ZIP. Não se incluem pesos dos modelos, livros didáticos integrais, ambiente Python instalado ou índice local ativo. O pacote compila o texto e permite auditar as evidências selecionadas; não substitui todos os insumos necessários à execução do protótipo.

A descrição do ambiente, os identificadores completos e as instruções de conferência estão em `poc/docs/MATERIAIS_E_REPRODUCAO.md`. O empacotamento é feito por `tools/package_overleaf.py`; o gerador histórico `tools/update_manuscript.py` teve sua escrita desativada.
