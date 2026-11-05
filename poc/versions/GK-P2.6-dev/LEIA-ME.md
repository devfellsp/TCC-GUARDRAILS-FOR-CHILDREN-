# GK-P2.6-dev — matérias do aluno fictício

Perfil: nove anos, quarto ano, português brasileiro. Dez chats: Língua Portuguesa, Matemática, Ciências, História, Geografia, Arte, Educação Física, Língua Inglesa, Tecnologia e Inovação e Geral. A lista representa os componentes presentes nos materiais selecionados, sem presumir uma escola real.

Execute poc/Iniciar_GuardKids_Atual.cmd na raiz e abra http://127.0.0.1:8770. Os modelos qwen3:8b e bge-m3:latest devem estar instalados no Ollama. O iniciador abre o serviço Ollama quando necessário, confere os modelos e restaura o índice preservado automaticamente quando falta o índice ativo. Comandos anteriores mantêm suas versões. Use somente um chatbot por vez para evitar concorrência dos modelos.

## Acervo

Esta versão mantém os recortes da GK-P2.5 e acrescenta seleções dos volumes 1 e 2 de Trilhas de Aprendizagens (2021), volumes 2 e 3 do Livro do Estudante/Currículo em Ação (arquivo de 2024), Material Rioeduca 4º ano (2026) e Caderno de Atividades de Campos, 4º ano, edição revisada (2025). São seis PDFs únicos e três sínteses anteriores.

O manifesto registra páginas impressas e de PDF, URL, hash do arquivo, âncoras e hash de cada novo recorte. SELECAO_DO_ACERVO.json contém os textos selecionados e exemplos. A seleção é documental assistida; não há certificação pedagógica independente nem autorização irrestrita para redistribuir obras e conteúdos de terceiros. Os arquivos completos permanecem no ambiente de pesquisa; sua presença pública não deve ser presumida como licença aberta.

A busca filtra a matéria antes de escolher os trechos mais próximos. Cada chat tem cobertura limitada aos temas indicados na interface. Não representa um curso completo, solucionador geral de exercícios ou interpretação automática de imagens. Educação Física usa recortes conceituais; instruções de uso de ferramentas, experiências arriscadas, exercícios com lacunas e legendas isoladas foram excluídos das novas seleções.

## Proteção, prazos e registros

A proteção de entrada, o controle de vocabulário ancorado, a conferência de sustentação, a proteção de saída e a persistência anterior à exibição continuam obrigatórios em todas as matérias. Inglês usa exemplos bilíngues ancorados, sem liberar tradução livre não sustentada. Não há memória entre perguntas.

O prazo total é de 600 segundos e a interface espera 10 segundos adicionais. Em CPU, uma resposta pode levar vários minutos. Os registros manuais omitem perguntas, respostas e justificativas em texto livre. Os testes fictícios desta ampliação são verificações de desenvolvimento, sem se tornarem resultados da avaliação final.

Recriar índice: poc/.venv/Scripts/python.exe -B poc/versions/GK-P2.6-dev/guardkids.py index
Restaurar índice: poc/.venv/Scripts/python.exe -B poc/versions/GK-P2.6-dev/restore_index.py

Os leitores PDF são fechados após cada fonte, e o modelo de embeddings é liberado depois da busca para reduzir a memória ocupada durante a geração em CPU. O modelo, os vetores, o limiar de busca e as regras de proteção são os mesmos.
