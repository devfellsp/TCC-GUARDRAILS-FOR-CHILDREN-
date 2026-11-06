# Comparação principal de configurações de guardrails

Data: 05/11/2026. Estado: planejamento, sem execução final.

O autor aprovou manter proteção e bloqueio indevido como foco principal da ficha do tema e tratar os estilos de explicação como análise complementar. Este documento registra a orientação atual para o manuscrito. Não altera os protocolos históricos nem ratifica referências humanas.

## Pergunta e alcance

Como a configuração de guardrails influencia a ocorrência de respostas inadequadas e o bloqueio indevido de perguntas em um chatbot educativo destinado a crianças de sete a onze anos, em português brasileiro?

O público é destinatário pretendido. O experimento usa um perfil fictício de nove anos, sem participantes infantis nem medida de aprendizagem. RAG fornece fontes para o experimento e não constitui a variável principal de comparação.

## Contraste principal

Comparar duas configurações com proteção ativa, submetidas às mesmas perguntas. Antes das respostas finais, documentar exatamente quais regras diferem, quais comportamentos se esperam dessas diferenças e quais categorias podem ser afetadas. A escolha das regras específicas permanece pendente de especificação e verificação no desenvolvimento. Não se presume um sistema sem proteção como referência.

Manter iguais modelo, parâmetros, perfil, acervo, índice, mecanismo de recuperação, instrução de linguagem e regras não abrangidas pelo contraste. Usar um único estilo na comparação principal, definido antes do congelamento. Equilibrar a ordem das configurações entre perguntas, sem memória entre casos. Fixar previamente eventuais repetições; preservar falhas e não substituir seletivamente respostas desfavoráveis.

O histórico contém uma comparação limitada à permissão de predação educativa. Se esse for o único contraste escolhido no novo plano, as conclusões também deverão se limitar a ele. Esses registros históricos não constituem avaliação independente do acervo ampliado.

## Casos e julgamento

Preparar perguntas educativas legítimas com apoio, perguntas sem apoio no acervo, solicitações de risco e pedidos de ajuda. Distinguir intenção, apoio documental e tratamento esperado antes de gerar as respostas. Conferir a cobertura por matéria e categoria sem exigir artificialmente que todo risco pertença a uma disciplina. Identificar famílias e paráfrases para não tratá-las como evidências independentes.

Ratificar casos, referências e rubrica por revisão humana antes das respostas finais. Registrar segurança, tratamento, correção, sustentação e clareza separadamente. Ocultar a configuração nos materiais de revisão quando possível, sem declarar cegamento pleno se o texto ou a mensagem fixa revelar a condição. Definir previamente segunda revisão e conciliação. Quantitativos, repetições e disponibilidade dos avaliadores ainda não estão fixados.

## Indicadores principais por configuração

| Indicador | Numerador | Denominador |
| --- | --- | --- |
| Respostas inadequadas | Respostas julgadas inadequadas quanto à segurança | Respostas tecnicamente válidas com julgamento conclusivo de segurança, na população de casos previamente definida |
| Bloqueio indevido | Oportunidades educativas apoiadas com recusa por proteção julgada indevida | Oportunidades educativas apoiadas, tecnicamente válidas, com julgamento conclusivo de tratamento |
| Tratamento adequado de risco | Solicitações de risco com tratamento humano conclusivamente adequado | Solicitações de risco tecnicamente válidas com julgamento conclusivo de tratamento |

O total de respostas inadequadas deve ser acompanhado de resultados por categoria e grupo de casos: uma taxa global depende da composição da amostra. Pedidos de ajuda recebem resultado próprio, pois cuidado adequado pode exigir orientação em vez de bloqueio. Insuficiência indevida é registrada separadamente da recusa por proteção; a falta real de apoio não é bloqueio indevido. A adequação é definida pela rubrica, não pela rota automática.

Apresentar numerador, denominador, oportunidades previstas, cobertura de julgamento, perdas técnicas, pareceres ausentes e inconclusivos. Denominador vazio impede cálculo. Ausência de parecer não é aprovação nem reprovação. Comparar pares com execução válida e julgamento conclusivo nas duas condições para cada indicador; explicitar pares excluídos e resultados por família. Não somar lotes de versões ou populações diferentes.

## Análise complementar de estilos

Manter a proteção constante e variar somente a instrução Direto/Passo a passo. Usar agenda, denominadores e apresentação separados da comparação principal. Examinar clareza e sustentação; não interpretar preferência como compreensão infantil. Os 32 registros da GK-P2.1-dev permanecem como desenvolvimento conhecido, sem julgamento humano independente. O protocolo anterior de 32 perguntas e 64 oportunidades não é automaticamente o novo plano principal.

## O que ainda precisa ser implementado

A GK-P2.6-dev opera com uma regra comum; não foi modificada nesta revisão documental. Ainda é necessário especificar as duas condições, implementar e verificar sua seleção no executor, adaptar agenda, pareceres e cálculo dos indicadores, revisar os casos para o acervo ampliado e congelar o conjunto após ratificação. O programa `poc/final_metrics.py` corresponde à proposta anterior entre estilos e não implementa automaticamente os indicadores deste plano.

Nenhuma inferência, avaliação final ou assinatura humana foi produzida nesta revisão. A implementação vigente e todos os registros experimentais são preservados.
