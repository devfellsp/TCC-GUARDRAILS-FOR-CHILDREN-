# Diagramas do GuardKids — revisão visual de 04/11/2026

Os sete desenhos foram refeitos como diagramas vetoriais originais, com agrupamento por funções, cores discretas, conectores identificados e a mesma apresentação em SVG, PDF e Draw.io. O conteúdo corresponde à POC GK-P2.1-dev: regra comum, quatro chats, busca vetorial e dois estilos de linguagem. As três figuras do manuscrito usam os mesmos PDFs vetoriais, evitando versões visuais divergentes.

## Referências de organização visual

Foram examinados os PDFs fornecidos pelo autor:

- **Evidence-Grounded Dynamic Hierarchical RAG for Intent-Driven Network Softwarization and Management**, de Chin-Feng Lai, Po-Chih Liu e Hsiao-Hwa Chen, IEEE Communications Magazine, aceito para publicação em 2026, DOI 10.1109/MCOM.001.2600303. Figuras 1 e 2, páginas 3 e 6 do PDF: agrupamento em planos, setas de dependência e decisões explícitas. [Abrir referência](C:/Users/Filipe/Downloads/Evidence_Grounded_Dynamic_Hierarchical_RAG_for_Intent_Driven_Network.pdf).
- **GRAIL-RAG: A Multi-Layer Guardrails Architecture with Session-Aware Memory and Multi-Stage Retrieval for Document-Grounded QA**, ICVADV-2026. Figuras 1, 2 e 3, páginas 3 e 4 do PDF: organização modular, camadas e diferenciação de proteção, recuperação e geração. [Abrir referência](C:/Users/Filipe/Downloads/GRAIL_RAG_A_Multi_Layer_Guardrails_Architecture_with_Session_Aware-1.pdf).

As referências orientaram a linguagem gráfica. Nenhuma figura foi copiada; os blocos e fluxos foram desenhados para o código e o protocolo do GuardKids. Não se atribuem à POC busca híbrida, memória de sessão, re-ranking, recuperação hierárquica dinâmica ou execução de ações em redes presentes nos artigos. Não foram importadas métricas desses trabalhos.

## Leitura e convenções

Molduras tracejadas agrupam funções ou etapas de pesquisa. Retângulos representam componentes e mensagens; losangos representam decisões. Setas contínuas indicam fluxo e setas tracejadas, dependência entre preparação e consulta. Cores auxiliam a leitura: azul para processamento/proteção, verde para geração ou resposta, roxo para sustentação, âmbar para insuficiência e vermelho para intervenção. As legendas escritas preservam o significado em impressão sem cor.

Os desenhos descrevem comportamento esperado ou rotas implementadas, não garantias de proteção. Similaridade não prova apoio, resposta liberada não equivale a acerto e o mesmo modelo participa da geração e das verificações.

## Os sete diagramas

| Nº | Arquivo-base | Finalidade |
|---|---|---|
| 1 | `01_dilema_calibracao_guardrails` | Distinguir permissividade, restrição excessiva e análise contextual. São situações conceituais, não condições ativas de comparação. |
| 2 | `02_fluxo_classificacao_indicativa` | Relacionar descritores de risco, intenção, perfil e tratamento. Não representa classificação oficial do chatbot. |
| 3 | `03_arquitetura_conceitual_integrada` | Apresentar contexto, camadas de entrada/busca/geração e verificação/entrega, com persistência antes da saída. Usado na Figura 1 do TCC. |
| 4 | `04_protocolo_experimental_metodologia` | Separar histórico, desenvolvimento executado e avaliação final planejada, sem somar denominadores. Usado na Figura 3 do TCC. |
| 5 | `05_pipeline_5_etapas_guardkids` | Mostrar o caminho de uma pergunta, insuficiência, intervenção e erro técnico. É uma visão resumida; o diagrama 7 detalha a precedência. |
| 6 | `06_curadoria_e_indexacao_rag` | Distinguir preparação do índice e consulta; registrar oito trechos, filtragem por chat e validação de integridade. |
| 7 | `07_regra_protecao_comum` | Mostrar quando orientar, bloquear, gerar ou informar limite. Ajuda em perigo/sexual/ofensa/substâncias, autolesão e privacidade seguem o código. Usado na Figura 2 do TCC. |

O nome antigo do diagrama 7, que mencionava Referência e Ajustada, foi retirado dos diretórios ativos. A versão anterior completa está preservada no arquivo de histórico desta revisão.

## Arquivos e edição

- `Todos_os_Diagramas_TCC_GuardKids.drawio`: sete abas editáveis. Abra no aplicativo Draw.io ou diagrams.net. Componentes pertencem aos seus grupos e as conexões usam pontos de ligação quando há uma caixa na extremidade.
- `drawio/`: arquivos editáveis separados.
- `svg/`: versões vetoriais para inserção em outros documentos.
- `pdf/`: versões vetoriais usadas pelo manuscrito.
- `Diagramas_GuardKids_editaveis.zip`: pacote com Draw.io, SVG e PDFs individuais.
- `../output/pdf/Diagramas_GuardKids_revisados.pdf`: caderno com os sete desenhos.

O gerador é `gerar_diagramas_revisados.py`; `gerar_diagramas.py` continua como entrada de compatibilidade. É necessário Python com ReportLab e as fontes Arial do Windows. A geração desta revisão utilizou o ambiente de documentos fornecido pelo Codex. Os textos e coordenadas são definidos uma vez e exportados aos três formatos; ajustes permanentes devem ser feitos nessa especificação. Alterações manuais em Draw.io precisam ser preservadas antes de regenerar os arquivos.

## Verificação

Os desenhos foram renderizados e conferidos visualmente, incluindo as três figuras em tamanho de página no TCC. A geração verifica largura e altura dos textos nas caixas. A estrutura XML, a quantidade de abas e a presença dos PDFs no pacote Overleaf são conferidas separadamente. O manuscrito foi recompilado depois da substituição das figuras. Não houve alteração do modelo, dos prompts, dos casos de teste ou do funcionamento da POC.
