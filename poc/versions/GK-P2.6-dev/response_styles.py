"""Políticas de apresentação, independentes das decisões de proteção."""
RESPONSE_STYLES = {
    "padrao": {
        "label": "Direto",
        "instruction": "Explique de forma direta, com frases curtas e termos definidos, em até 120 palavras.",
    },
    "passo_a_passo": {
        "label": "Passo a passo",
        "instruction": (
            "Explique para uma criança de 9 anos em português brasileiro simples e acolhedor. "
            "Produza de uma a três afirmações curtas no campo claims, uma ideia por afirmação. "
            "O programa numera essas afirmações; não escreva números, introdução ou conclusão. "
            "Não há exigência de exemplo nem de preencher três afirmações. "
            "Só use um exemplo se estiver explicitamente nos trechos; não invente situações hipotéticas. "
            "Prefira palavras do dia a dia. Se precisar de um termo novo, "
            "explique seu significado na mesma frase. Não acrescente processos ou detalhes que "
            "a pergunta não exige. Evite jargão, diminutivos excessivos, voz de bebê e elogios automáticos. "
            "Exemplos também precisam estar sustentados pelos trechos: não invente fatos, experiências "
            "ou recomendações para tornar a explicação divertida. Não diga que realizou uma experiência. "
            "A simplicidade não pode mudar o significado nem dispensar fontes ou proteções."
        ),
    },
}
