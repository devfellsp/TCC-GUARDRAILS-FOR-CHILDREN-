# Matriz de atendimento ao parecer de 03/11/2026

Etapa confirmada pelo autor: **Projeto/TCC I**. O parecer enumera 16 subitens (1.1–5.4), todos relacionados abaixo. “Preparado” indica material pronto para uma atividade ainda não executada; não equivale a validação humana. As localizações abaixo são da versão modular revisada; as localizações antigas estão no parecer original preservado.

| ID | Pendência e localização atual | Ação realizada | Evidência verificável | Situação |
|---|---|---|---|---|
| 1.1 | Resumo/abstract, `main.tex` | Retiradas afirmações de preservar proteção/eliminar recusas; resultados técnicos e avaliação pendente separados nos dois idiomas | Resumos e `texto/05_evidencias.tex` | Corrigido no texto |
| 1.2 | Título, introdução, conclusão | Título delimita Ciências do quarto ano; 7–11 é destinação, perfil fictício nove anos, sem crianças participantes | `main.tex`; `texto/01_introducao.tex`; `06_consideracoes.tex` | Corrigido no texto |
| 1.3 | Preâmbulo, objetivos, continuidade | Etapa TCC I, matriz de objetivos e cronograma de realizado/planejado | Cap. 6, tabelas de objetivos e cronograma; `revisao_origem.json` | Corrigido; aceite institucional externo |
| 2.1 | Metodologia, comparação | Referência explicada como ablação; E1–E3 verificáveis; pedidos mistos e contrastes de intenção | Cap. 3; `PROTOCOLO.md`; casos R01 e P03 | Preparado; avaliação final pendente |
| 2.2 | Amostra e execução | 40 perguntas/20 famílias; 160 oportunidades; origem/exposição/repetições/ordem/perdas e orçamento explícitos | `protocolo.json`; casos; `poc/evaluation.py`; chave de agenda | Preparado; capacidade humana a confirmar |
| 2.3 | Apoio versus recuperação | Apoio definido por leitura, com dados temáticos ausentes e categoria independente da similaridade | `corpus_referencia.json`; G3; Cap. 3 | Proposta conferida com assistência de IA; ratificação humana pendente |
| 2.4 | Parâmetros | Justificativas operacionais; sondagem real 0,35/0,45/0,55 só no desenvolvimento; limites não otimizados declarados | `evidencias/calibracao_desenvolvimento.json`; tabela de parâmetros | Sondagem realizada; sem alegação de ótimo |
| 3.1 | Julgamento | Rubrica com níveis, desempates, exemplos, verdade sem apoio, autoria/data e revisão secundária; cópia sem condições | `RUBRICA.md`; dois XLSX; 32 linhas secundárias na chave | Instrumentos preparados; nenhum julgamento humano inventado |
| 3.2 | Indicadores | Segurança/atendimento separados; contagens por grupo/categoria, ASCS, diferenças pareadas, perdas e não executadas | `poc/metrics.py`; aba Indicadores; testes de métricas | Implementado e testado; taxas finais pendentes |
| 4.1 | Políticas | Ajuda versus dano; sete categorias incluindo injeção; `help_seeking` obrigatório na GK-P1.2 | Cap. 4; classificador; testes; 12/12 rotas de ajuda e 4/4 controles no desenvolvimento | Corrigido e verificado em desenvolvimento; generalização não demonstrada |
| 4.2 | Currículo | BNCC oficial EF04CI04/06 com vínculo de objetivos, recortes e famílias | Tabela curricular; PDF e hash oficiais em fontes/ | Conferido documentalmente; revisão pedagógica especializada pendente |
| 4.3 | Acervo | Descrições dos cinco recortes reais, excluídos termos indevidamente atribuídos aos blocos | Tabela do corpus; JSON com texto/hash do índice | Corrigido; direitos e revisão científica especializada pendentes |
| 5.1 | Fundamentação | Busca narrativa realmente executada e registrada; metadados primários; NeMo/Llama Guard como inspirações | `BUSCA_NARRATIVA.md`; Cap. 2; referências | Corrigido; sem alegação de exaustividade |
| 5.2 | Versão | Fluxo unificado, quatro chamadas, índice ativo, âncoras e registros minimizados; históricos separados | Cap. 4; algoritmo/figuras; congelamentos e snapshots | Alinhado ao código; versões antigas preservadas |
| 5.3 | Discussão | Afirmações qualificadas; documentadas falhas de ajuda, decomposição/predação e sustentação; detalhes operacionais no apêndice | Cap. 5 e 6; registros reais dos dois lotes | Corrigido; falhas do classificador permanecem limitação observada |
| 5.4 | Apresentação | Três figuras chamadas no texto, listas, instituição, quatro palavras-chave, etapa e cronograma; sem banca fictícia; consulta ao manual | PDF conferido, fontes, instruções Overleaf e logs de compilação | Revisado; aprovação/formalização institucional externas |

As pendências humanas não impedem a entrega como projeto delimitado, mas impedem declarar concluída a avaliação comparativa de segurança/qualidade. Os instrumentos permitem sua continuidade sem alterar retroativamente os resultados de desenvolvimento.
