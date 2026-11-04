# Ajuste de configuração de compilação

Erro informado pelo autor: `fontspec cannot-use-pdftex`, ao compilar no Overleaf com pdfLaTeX. A versão do texto utiliza fontes OpenType e requer XeLaTeX (ou configuração compatível com LuaLaTeX); a versão verificada usa XeTeX.

Adicionadas indicações do compilador aos arquivos de entrada e aos geradores, `latexmkrc` com `$pdf_mode = 5` (padrão XeLaTeX) e instruções para selecionar XeLaTeX no Overleaf. A opção do editor deve ser conferida manualmente; não se afirma que importar um ZIP altera a configuração do projeto remoto. Não houve acesso à conta ou alteração remota do Overleaf.

O conteúdo acadêmico, os casos, a inferência e os resultados permanecem os da entrega anterior. O pacote Overleaf e a entrega completa foram regenerados. Originais dos arquivos alterados preservados em `historico/Antes_ajuste_compilador_20261103.zip`.
