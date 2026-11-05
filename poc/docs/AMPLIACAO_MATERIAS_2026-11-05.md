# Ampliação da PoC por matéria — 05/11/2026

A GK-P2.6-dev disponibiliza dez chats para o perfil fictício de nove anos, quarto ano. Iniciador: poc/Iniciar_GuardKids_Atual.cmd. Endereço: http://127.0.0.1:8770.

## Acervo implementado

Seis PDFs de quatro coleções: Trilhas de Aprendizagens (volumes 1 e 2, 2021), Livro do Estudante/Currículo em Ação (volumes 2 e 3, arquivos de 2024), Rioeduca (4º ano, 2026) e Caderno de Atividades de Campos (4º ano, 2025 revisado). Mantidas as três sínteses anteriores. O corpus tem 40 blocos; foram acrescentados 21 recortes, um deles dividido em dois blocos, aos 18 anteriores.

Os novos trechos têm arquivo, página impressa, página de PDF, âncoras e hash do texto normalizado. O manifesto também identifica a origem dos quatro novos PDFs. A revisão é documental assistida; revisão pedagógica independente e ratificação dos direitos de terceiros permanecem pendentes. Acesso público não foi tratado como licença aberta irrestrita.

## Matérias e escopo

Português: fábula e crônica. Matemática: frações, comprimento e operação inversa. Ciências: alimentação, cadeias alimentares, decomposição, vidro e recursos naturais. História: fontes, memória, nomadismo, agricultura e trocas. Geografia: paisagem, mapas, migração, matérias-primas e produção. Arte: cultura popular, cantigas e um recorte sobre Romero Britto. Educação Física: esportes de invasão, basquete e forró. Inglês: THERE IS/ARE, frequência e um diálogo de restaurante. Tecnologia: protótipos, wiki e repetição. Geral: organização, convivência, privacidade e curiosidades apoiadas no acervo.

A separação por matéria ocorre antes do top-k. A API rejeita matérias desconhecidas, e a interface obtém as opções da mesma lista do servidor. A troca de matéria limpa resposta, fontes e identificador anteriores. Todas passam pelas mesmas verificações e pela gravação anterior à exibição.

## Verificações

Passaram 25 testes Python e um teste da interface em Node, abrangendo isolamento por matéria, proteção de dados em todos os chats, entrada inválida, origem não autorizada, fontes inventadas, integridade do acervo e restauração sem inferência.

Três consultas reais pela API, em Português, Matemática e Inglês, terminaram como allow, valid=true e com fonte. Os tempos foram, respectivamente, 303,546 s, 115,096 s e 248,340 s. São verificações fictícias de desenvolvimento; não foram incorporadas à avaliação final nem aos resultados anteriores. Os detalhes estão em GK-P2.6-dev/VERIFICACAO_LOCAL.json.

Depois dessas consultas, o fechamento explícito dos leitores PDF e a liberação do modelo de embeddings após a busca foram aplicados para reduzir memória. Os 25 testes e o teste da interface foram repetidos e passaram. Uma busca real confirmou o mesmo índice e apenas fontes de Português; o BGE-M3 estava descarregado depois da operação. A API final respondeu ready=true com as dez matérias. O índice e os vetores permaneceram idênticos; o ajuste afeta a gestão de recursos.

O iniciador confere os modelos, inicia o Ollama quando necessário e restaura o índice preservado se faltar o índice ativo. O prazo total é de 600 segundos, com 10 segundos adicionais no navegador. Em CPU, as verificações podem levar vários minutos.

A ampliação está em uma versão própria. O manuscrito, seus diagramas, os protocolos reservados e os resultados anteriores não foram atualizados por esta implementação.
