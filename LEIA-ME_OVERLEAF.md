# Prova de conceito com guardrails — Projeto/TCC I multidisciplinar

Versão atualizada em 04/11/2026: regra comum, 32 tentativas de desenvolvimento efetivamente executadas e plano final de 32 perguntas/64 oportunidades ainda não executado. Os 108 registros anteriores permanecem em seção histórica, com denominadores próprios. A inspeção preliminar do conteúdo não equivale à ratificação humana independente.

1. Importe `Overleaf_TCC_Drawio_rotulos.zip` como novo projeto no Overleaf.
2. Abra **Settings/Configurações** pelo ícone de engrenagem (ou menu **File → Settings**). Em **Compiler/Compilador**, selecione **XeLaTeX**. Confirme `main.tex` como documento principal. Em interfaces anteriores, essas opções ficam em **Menu → Settings**. TeX Live 2025 ou posterior é recomendado; não foi executada compilação no serviço Overleaf nesta revisão.
3. Compile novamente se necessário para atualizar sumário, listas e referências. A entrada `document.tex` apenas carrega `main.tex`.
4. Edite os capítulos em `texto/`. As sete figuras usam PDFs vetoriais em `diagramas/pdf/`, incluídos no pacote. Os originais editáveis estão em `diagramas/drawio/`. Cada PDF tem o mesmo nome-base que a fonte individual. O arquivo com sete abas reúne os mesmos desenhos. Para alterar uma figura, edite-a no Draw.io, atualize também a aba correspondente do arquivo conjunto e exporte o desenho como PDF no caminho indicado no LaTeX. Preserve ambas as pastas ao importar no Overleaf. As tabelas `generated/development_*.tex` são geradas das evidências locais, não contêm julgamentos humanos. Não as trate como resultados finais.

O pacote é autossuficiente para compilar o texto; não precisa dos modelos nem PDFs didáticos. Utiliza abnTeX2, fontspec, TikZ, pgfgantt e algorithm2e. A revisão inclui as fontes Times New Roman em fontes/ para manter a mesma composição na cópia de trabalho e no pacote pessoal do autor. Preserve essa pasta ao compilar; sem ela, o preâmbulo utiliza TeX Gyre Termes como alternativa.

A edição atual foi recompilada localmente com Tectonic (motor XeTeX), a partir de extração limpa do ZIP. No Overleaf, selecione XeLaTeX. A nota de entrega da edição com sete figuras registra as verificações desta revisão. A ratificação de referências, a revisão humana de conteúdo e a avaliação final estão pendentes. A ausência de banca/assinaturas nesta versão é intencional: não se declara aprovação de um Projeto/TCC I ainda em elaboração.

## Erro “fontspec requires either XeTeX or LuaTeX”

Esse erro indica que o projeto está sendo processado por pdfLaTeX/LaTeX. Mude o compilador para **XeLaTeX** nas configurações do projeto e clique em **Recompile**. O `fontspec` é necessário às fontes OpenType usadas nesta versão.

Não é necessário reenviar os arquivos para corrigir um projeto já importado. Se o log ainda indicar pdfTeX após a mudança, confirme que alterou o compilador do projeto correto e selecione **Recompile from scratch** no menu de recompilação.

O pacote inclui a indicação `% !TeX program = xelatex` nos arquivos de entrada e `latexmkrc` com XeLaTeX como padrão. Essas indicações não substituem a conferência da opção **Compiler** no Overleaf: configurações explícitas do editor podem prevalecer sobre padrões de arquivo.

Os avisos de depreciação de `babel`/`memoir` não são a causa desse erro fatal de compilador. Não é necessário modificar o texto acadêmico para resolver o problema mostrado.

Orientação conferida na [documentação oficial do Overleaf](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler).

## Notas de preparação do documento

O manual disponível no portal do curso foi consultado na revisão (UNITINS, 2025). Ajustaram-se denominação institucional, quatro palavras-chave, margens, recuo, espaçamento e apresentação. O arquivo utiliza os arquivos Times New Roman da pasta fontes/. Os resumos usam 11 pontos; o texto principal, 12 pontos. As sete figuras do Draw.io foram preservadas, com identificação acima e fonte abaixo. A compilação e a inspeção visual não constituem certificação integral de conformidade com ABNT ou com o manual.

Essas informações documentam a edição e não integram o conteúdo acadêmico do PDF. O histórico de alterações, os backups e a matriz de atendimento ao parecer ficam nos materiais de acompanhamento, fora dos capítulos e apêndices da pesquisa.

A revisão prospectiva de 04/11/2026 define o ASCS, equilibra a segunda revisão dentro de cada chat e tipo de caso e acrescenta o formulário de preferência pareada de clareza. Nenhuma resposta final ou assinatura humana foi produzida. A versão atual do PDF tem 41 páginas. O script histórico de métricas não implementa o novo protocolo.

O ASCS prospectivo possui calculador próprio em `poc/final_metrics.py`, com verificação documental e taxas condicionadas à revisão humana encerrada. Seu código acompanha o pacote; não é necessário executá-lo para compilar o manuscrito.

O cronograma usa o modelo de Gantt em `texto/cronograma.tex`, com o pacote `pgfgantt`, intervalos quinzenais e 16 atividades entre outubro/2026 e junho/2027. As barras distinguem desenvolvimento realizado de continuidade proposta. O manuscrito passa a ter oito figuras (sete Draw.io e um Gantt) e dez tabelas.

O manuscrito não contém apêndice operacional. Seu conteúdo foi transferido para `poc/docs/MATERIAIS_E_REPRODUCAO.md`, incluído no pacote como documentação de apoio.

## Materiais suplementares incluídos

Além das fontes editoriais, o ZIP inclui o lote multidisciplinar completo arquivado (agenda, resultados, revisão, 32 registros completos, snapshot, ambiente e manifesto SHA-256), os dois lotes históricos de Ciências e seus congelamentos. Os instrumentos reservados permanecem em branco. O PDF principal é entregue separadamente e não integra o ZIP. Não se incluem pesos dos modelos, livros didáticos integrais, ambiente Python instalado ou índice local ativo. O pacote compila o texto e permite auditar as evidências selecionadas; não substitui todos os insumos necessários à execução do protótipo.

A descrição do ambiente, os identificadores completos e as instruções de conferência estão em `poc/docs/MATERIAIS_E_REPRODUCAO.md`. O empacotamento é feito por `tools/package_overleaf.py`; o gerador histórico `tools/update_manuscript.py` teve sua escrita desativada.
