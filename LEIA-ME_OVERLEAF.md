# Prova de conceito com guardrails — Projeto/TCC I multidisciplinar

Versão atualizada em 04/11/2026: regra comum, 32 tentativas de desenvolvimento efetivamente executadas e plano final de 32 perguntas/64 oportunidades ainda não executado. Os 108 registros anteriores permanecem em seção histórica, com denominadores próprios. A revisão de conteúdo atual é assistida por IA, não ratificação humana.

1. Importe `Overleaf_TCC_PoC.zip` como novo projeto no Overleaf.
2. Abra **Settings/Configurações** pelo ícone de engrenagem (ou menu **File → Settings**). Em **Compiler/Compilador**, selecione **XeLaTeX**. Confirme `main.tex` como documento principal. Em interfaces anteriores, essas opções ficam em **Menu → Settings**. TeX Live 2025 ou posterior é recomendado; não foi executada compilação no serviço Overleaf nesta revisão.
3. Compile novamente se necessário para atualizar sumário, listas e referências. A entrada `document.tex` apenas carrega `main.tex`.
4. Edite os capítulos em `texto/`. As três figuras usam PDFs vetoriais em `diagramas/pdf/`, incluídos no pacote. Preserve essa pasta ao importar no Overleaf. As tabelas `generated/development_*.tex` são geradas das evidências locais, não contêm julgamentos humanos. Não as trate como resultados finais.

O pacote é autossuficiente para compilar o texto; não precisa dos modelos nem PDFs didáticos. Utiliza abnTeX2, fontspec, TikZ e algorithm2e. No Windows usa Times New Roman instalada; em ambiente sem essa fonte usa TeX Gyre Termes, compatível visualmente mas não idêntica. Conferir exigência de fonte com orientador antes da entrega institucional. Não redistribuir arquivos de fonte proprietária sem licença.

A versão foi verificada localmente com Tectonic 0.17.0/XeTeX. A compilação foi concluída e o PDF foi inspecionado visualmente. A ratificação de referências, a revisão humana de conteúdo e a avaliação final estão pendentes. A ausência de banca/assinaturas nesta versão é intencional: não se declara aprovação de um Projeto/TCC I ainda em elaboração.

## Erro “fontspec requires either XeTeX or LuaTeX”

Esse erro indica que o projeto está sendo processado por pdfLaTeX/LaTeX. Mude o compilador para **XeLaTeX** nas configurações do projeto e clique em **Recompile**. O `fontspec` é necessário às fontes OpenType usadas nesta versão.

Não é necessário reenviar os arquivos para corrigir um projeto já importado. Se o log ainda indicar pdfTeX após a mudança, confirme que alterou o compilador do projeto correto e selecione **Recompile from scratch** no menu de recompilação.

O pacote inclui a indicação `% !TeX program = xelatex` nos arquivos de entrada e `latexmkrc` com XeLaTeX como padrão. Essas indicações não substituem a conferência da opção **Compiler** no Overleaf: configurações explícitas do editor podem prevalecer sobre padrões de arquivo.

Os avisos de depreciação de `babel`/`memoir` não são a causa desse erro fatal de compilador. Não é necessário modificar o texto acadêmico para resolver o problema mostrado.

Orientação conferida na [documentação oficial do Overleaf](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler).

## Notas de preparação do documento

O manual disponível no portal do curso foi consultado na revisão (UNITINS, 2025). Ajustaram-se denominação institucional, quatro palavras-chave, margens, recuo, espaçamento e apresentação. O arquivo utiliza Times New Roman quando preparada a cópia local da fonte no Windows e TeX Gyre Termes no ambiente portátil do Overleaf. A fonte usada deve ser conferida na entrega institucional. A compilação e a inspeção visual não constituem certificação integral de conformidade com ABNT ou com o manual.

Essas informações documentam a edição e não integram o conteúdo acadêmico do PDF. O histórico de alterações, os backups e a matriz de atendimento ao parecer ficam nos materiais de acompanhamento, fora dos capítulos e apêndices da pesquisa.
