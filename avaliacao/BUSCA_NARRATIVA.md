# Registro de busca narrativa — 03/11/2026

Objetivo: situar proteção contextual em chatbots para menores e conferir referências do projeto. Seleção narrativa intencional, não revisão sistemática. Operação assistida por IA; interpretação do pesquisador/orientador ainda necessária. Idiomas considerados: português e inglês; período de interesse 2020–2026 para literatura, admitindo BNCC de 2018 por finalidade curricular. Não se usaram filtros automáticos de data nas consultas; datas foram conferidas nas fontes selecionadas.

## Acesso e consultas efetivamente executadas

Busca web, seguida de acesso às fontes primárias. Não se afirma consulta direta às interfaces de Scopus, Google Scholar, Web of Science ou bases pagas.

1. `"child" "guardrails" "Portuguese" LLM educational chatbot`
2. `"MinorBench" "children" benchmark 2025`
3. `"LLM Safety for Children" Rath`
4. `"guardrails" "chatbot" "infantil" português`
5. `site:unitins.br "manual" "TCC" "Sistemas de Informação"`
6. `site:unitins.br "2025" "manual" "TCC"`
7. `site:gov.br "BNCC_EI_EF_110518"`
8. `site:gov.br "classind-audio-visual-2025-vs-10-nova-faixa.pdf"`
9. `"Informing Age-Appropriate AI" Wang Zhao 2022`
10. `site.gov.br "Classificação Indicativa" "2025" "quinta"` (registrado com ponto após `site`, exatamente como enviado, sem presumir filtragem efetiva)
11. `site.arxiv.org "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"` (mesma limitação de sintaxe)

Também houve abertura por URL de referências já conhecidas para conferir metadados: Rath, NeMo, MinorBench, Llama Guard, manual, BNCC, ClassInd e referencial curricular do Paraná. Uma tentativa de localizar Wang por `arxiv.org/abs/2203.17142` abriu um artigo de astronomia: excluído por erro de identificador, sem uso como evidência. A consulta por título encontrou a publicação correta via DOI e Oxford.

## Critérios de seleção e limitações

Incluir estudos primários sobre riscos de conteúdo para menores ou arquitetura de salvaguardas/RAG, com autoria verificável; incluir documentos oficiais para currículo e apresentação institucional. Conferir referências já presentes no projeto, sem transformar citações secundárias em evidência primária. Excluir publicidade sem método, resultados de redes sociais, materiais irrelevantes e duplicatas. A análise não contabiliza universo de resultados: a ferramenta não forneceu conjunto estável/exaustivo, e não foi feito rastreio sistemático de todos os achados.

## Fontes selecionadas e decisão

| Fonte primária | Uso no trabalho | Conferência |
|---|---|---|
| [Rath et al., ACL 2025](https://aclanthology.org/2025.naacl-industry.62/) | Riscos/perfis infantis; limites de generalização | Autores, publicação formal NAACL Industry, pp. 809–821 e DOI 10.18653/v1/2025.naacl-industry.62. Corrigida identificação anterior de apenas preprint. Não se misturam estatísticas de versões. |
| [MinorBench, arXiv v1](https://arxiv.org/abs/2503.10242) | Inspiração de categorias; casos próprios | Khoo, Chua, Shong; 13/03/2025. Nenhuma tradução literal ou validação do benchmark declarada. |
| [NeMo, ACL 2023](https://aclanthology.org/2023.emnlp-demo.40/) | Inspiração arquitetural | pp. 431–445, DOI 10.18653/v1/2023.emnlp-demo.40. Não implementado. |
| [Llama Guard, arXiv](https://arxiv.org/abs/2312.06674) | Inspiração de entrada/saída | Autoria Inan et al.; 2023; não executado no GuardKids. |
| [Wang et al., ACM/DOI](https://doi.org/10.1145/3491102.3502057) e [repositório dos autores em Oxford](https://ora.ox.ac.uk/objects/uuid%3A98022d77-3b32-4f06-a4a7-a624aa564b33/files/s3484zh77q) | Princípios apropriados à idade | CHI 2022, artigo 536, 29 páginas. Nenhum percentual transferido ao protótipo. |
| [Lewis et al., arXiv](https://arxiv.org/abs/2005.11401) | Conceito RAG | 2020; inspiração, sem reprodução do treinamento original. |
| [BNCC/MEC](https://basenacionalcomum.mec.gov.br/images/BNCC_EI_EF_110518_versaofinal_site.pdf) | EF04CI04 e EF04CI06 | PDF baixado, SHA-256 em fontes/downloads.json; p. impressa 339. Conferidos códigos e vínculo às cadeias alimentares/decomposição. |
| [Ciências 4º ano, Paraná](https://www.referencialcurriculardoparana.pr.gov.br/Ciencias-4o-Ano) | Conferência complementar | A matriz do texto usa a BNCC nacional, sem declarar adoção do currículo paranaense pelo curso/escola. |
| [Guia ClassInd/MJSP](https://www.gov.br/mj/pt-br/assuntos/seus-direitos/classificacao-1/classind-audio-visual-2025-vs-10-nova-faixa.pdf/view) | Referência contextual | Portal oficial do guia de 2025; arquivo original já presente no projeto. Não se realiza enquadramento regulatório oficial. |
| [Manual UNITINS](https://www.unitins.br/cms/Arquivos/Download/D5D2798C96CF7CE88B0DBDD1CB2AE0174CC49043) | Etapa e apresentação | Vinculado no [portal do curso](https://unitins.br/nPortal/sistemas-de-informacao-palmas); capa 2025, histórico interno 2024. Baixado e conferido, pp. 14–19 sobre apresentação; resumo 150–250 palavras e quatro palavras-chave. Não se declara certificação ABNT integral. |

O mecanismo também encontrou uma [notícia oficial de 15/10/2026 sobre novo guia de usos de IA na infância](https://www.gov.br/mj/pt-br/assuntos/noticias/mjsp-e-mdhc-lancam-guia-sobre-usos-da-inteligencia-artificial-na-infancia-e-adolescencia/). A notícia foi aberta, mas o guia completo não foi analisado nesta revisão; achado registrado para continuidade, sem atribuir-lhe recomendações específicas nem alterar silenciosamente políticas com base no título.

Martínez et al. e métricas lexicais foram retirados do argumento central porque não são medidos no protocolo atual. Os arquivos e a referência original permanecem no backup. Isso reduz a promessa metodológica, sem desqualificar o estudo. Não foi feita nova alegação de inexistência de pesquisas em português.

## Evidência local

`fontes/downloads.json` conserva URLs, tamanho e hashes dos downloads oficiais de BNCC e manual. `fontes/bncc_habilidades.txt` registra a extração da página relevante; a extração de PDF foi conferida para códigos/conteúdo, sem substituir inspeção do documento. A atribuição da obra SEDUC-SP 2024 deriva do exemplar e manifesto locais; suas condições de reutilização exigem conferência antes de redistribuir o corpus. O pacote de entrega não inclui os PDFs didáticos completos nem pesos dos modelos.

## Consulta complementar para a revisão do capítulo 2 — 04/11/2026

Foram conferidas as publicações primárias abaixo, selecionadas para esclarecer três decisões que o levantamento inicial não desenvolvia. Esta consulta dirigida complementa a busca narrativa de 03/11, sem alterar retrospectivamente seu registro ou transformar a revisão em sistemática.

- Recuperação densa: consulta por BGE-M3, Chen e ACL. [Chen et al. (2024)](https://aclanthology.org/2024.findings-acl.137/) fundamenta a distinção entre as capacidades do modelo e a recuperação efetivamente usada na PoC.
- Sustentação de respostas: consulta por ALCE, geração com citações e Gao. [Gao et al. (2023)](https://aclanthology.org/2023.emnlp-main.398/) distingue fluência, correção e qualidade das citações.
- Linguagem escolar: consulta por compreensão de conectivos no ensino primário. [Volodina e Weinert (2020)](https://doi.org/10.3389/fpsyg.2020.00814) investigam relações linguísticas em uma amostra alemã; o estudo não avalia chatbots ou estudantes brasileiros.
