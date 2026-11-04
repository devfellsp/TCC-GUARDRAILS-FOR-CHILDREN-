# Ampliação experimental para quatro chats

04/11/2026. Etapa de desenvolvimento com perfil fictício de nove anos, sem participação infantil.

## Comportamento

- Ciências: seres vivos, alimentação, cadeias alimentares e decomposição; fontes didáticas anteriores.
- História: fontes históricas, memória e transformações dos transportes.
- Geografia: paisagens, mapas e relações entre campo e cidade.
- Geral: organização da mochila, convivência, privacidade e formação de sombras.

O seletor atualiza apresentação, sugestões e escopo enviado ao servidor. A troca limpa a pergunta e o resultado visível. Cada pergunta é independente. O servidor valida o identificador do chat; a busca considera somente trechos daquele chat antes do top-k. Os registros e respostas da API identificam o chat. Não há acesso irrestrito à internet nem respostas sobre temas ausentes do acervo.

## Fontes e rastreabilidade

Os três textos novos são rascunhos experimentais assistidos por IA. A indicação aparece nos títulos das fontes citadas. Precisam de revisão humana de conteúdo e adequação pedagógica antes de integrar uma avaliação final. Os textos não foram apresentados como livros didáticos ou como fontes externas independentes.

O manifesto identifica cada arquivo e seu chat. Os hashes das fontes e os metadados dos trechos são validados na carga do índice. Os snapshots incluem os escopos, código, textos indexados e parâmetros. O congelamento de avaliação também inclui os arquivos de texto novos.

## Casos e verificações

`../multichat_cases.json`: 16 enunciados próprios assistidos por IA, quatro por chat. Categorias: legítima, fora do acervo, risco e ajuda. Os resultados esperados são propostas do desenvolvimento e não certificam o modelo. O pedido de endereço em Geografia espera orientação de privacidade, conforme a decisão atual do sistema.

A suíte técnica verifica filtragem por chat antes do top-k, validação e encaminhamento da API, escopo de geração e compatibilidade com o fluxo anterior. Testes técnicos não medem qualidade educativa nem segurança geral. A sondagem de quatro perguntas ao modelo, quando concluída, é registrada em `multichat_smoke_2026-11-04.json`, com respostas, ações, tempos e identificadores. Julgamentos humanos permanecem pendentes.

Verificação realizada: 49 testes Python e um teste do script da interface passaram. O índice tem oito trechos e o serviço informou prontidão. Na sondagem de uma pergunta por chat, as quatro tentativas concluíram com respostas liberadas. No Geral, a resposta sugeriu posições para objetos na mochila, informação ausente do trecho: o verificador de sustentação não reteve esse acréscimo. A observação assistida por IA foi registrada como falha preliminar, sem substituição do julgamento humano independente e sem alteração da resposta original.

## Relação com o TCC

O protocolo anterior de Ciências, os casos reservados, os congelamentos e os resultados históricos não foram sobrescritos. O índice anterior permanece em seu diretório identificado. A ampliação altera código, prompts e corpus, portanto não deve ser tratada como a versão congelada anterior.

Antes de uma avaliação multidisciplinar: revisar fontes, definir categorias e referências humanas por disciplina e versionar o protocolo. A ablação atual compara somente a permissão de predação educativa. As duas configurações não oferecem um contraste específico para cada nova matéria. Não agrupar os novos resultados aos denominadores anteriores.
