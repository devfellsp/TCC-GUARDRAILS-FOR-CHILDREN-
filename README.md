# TCC GuardKids — Guardrails Configuráveis para Chatbot Educativo Infantil

**Autor:** Filipe Martins Henrique  
**Orientador:** Prof. Marcos Souza  
**Curso:** Sistemas de Informação — Universidade Estadual do Tocantins (UNITINS)  
**Tema:** Desenvolvimento e avaliação de guardrails configuráveis em uma prova de conceito de chatbot educativo destinado a crianças de 7 a 11 anos em português brasileiro.

---

## Estrutura do Repositório

* [`Capitulo_3_Metodologia_Atualizado.tex`](./Capitulo_3_Metodologia_Atualizado.tex) / [`document.tex`](./document.tex): Código-fonte LaTeX (`abntex2`) do Capítulo 3 (Metodologia), contendo o Quadro de Políticas de Proteção, a Estrutura da Amostra de Avaliação e a Rubrica de Qualidade das Respostas.
* [`metodologia_guardkids_revisada.zip`](./metodologia_guardkids_revisada.zip): Pacote `.zip` pronto para importação direta no Overleaf.
* [`Cronograma.pdf`](./Cronograma.pdf): Cronograma de execução do projeto (Outubro/2026 a Junho/2027).
* [`ficha_tema_tcc_Filipe_Martins_Henrique_revisada.docx`](./ficha_tema_tcc_Filipe_Martins_Henrique_revisada.docx): Ficha de definição do tema, problema de pesquisa, objetivos e facetas metodológicas.
* [`artigos_e_guias/`](./artigos_e_guias/): Artigos científicos, guia de Classificação Indicativa (MJSP, 2025) e apostila escolar de referência (SME-SP, 2021).
  * `01_Artigo_MinorBench_Riscos_Infantis_Khoo_2025.pdf`
  * `02_Artigo_Seguranca_de_LLMs_Para_Criancas_Rath_2025.pdf`
  * `03_Artigo_Principios_IA_Para_Criancas_Wang_2022.pdf`
  * `04_Artigo_Vocabulario_Perfis_e_Parametros_LLM_Martinez_2024.pdf`
  * `05_Artigo_Base_RAG_Recuperacao_e_Geracao_Lewis_2020.pdf`
  * `06_Guia_Classificacao_Indicativa_Ministerio_da_Justica_2025.pdf`
  * `07_Apostila_Ciencias_4_Ano_Seres_Vivos_Trilhas_SP_2021.pdf`
* [`benchmarks_e_datasets/`](./benchmarks_e_datasets/): Bases de dados abertas utilizadas como referência.
  * `01_Benchmark_MinorBench_Perguntas_de_Risco/`: Dataset *MinorBench* (299 casos de risco infantil em 6 categorias).
  * `02_Dataset_Zenodo_Perfis_e_Parametros_Martinez_2024/`: Dataset do Zenodo (`10.5281/zenodo.11121394`) com avaliações de perfil etário (*role*) e parâmetros de geração (`temperature`, `top_p`, penalidades).
