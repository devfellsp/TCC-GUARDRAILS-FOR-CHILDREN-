"""Políticas de apresentação, independentes das decisões de proteção."""
RESPONSE_STYLES = {
    "padrao": {
        "label": "Direto",
        "instruction": "Explique de forma direta, com frases curtas e termos definidos, em até 120 palavras.",
    },
    "passo_a_passo": {
        "label": "Passo a passo · com exemplos",
        "instruction": (
            "Explique para uma criança de 9 anos em português brasileiro simples e acolhedor. "
            "No campo answer, siga este formato obrigatório, com quebras de linha: "
            "uma frase inicial que responde à dúvida; depois '1. ' e '2. ' com uma explicação curta "
            "em cada linha; por último 'Por exemplo: ' com uma situação concreta. "
            "Explique uma ideia por vez. Inclua um exemplo concreto "
            "ligado ao que os trechos sustentam; use até dois exemplos somente se ajudarem e couberem "
            "no limite de 120 palavras. Prefira palavras do dia a dia. Se precisar de um termo novo, "
            "explique seu significado na mesma frase. Não acrescente processos ou detalhes que "
            "a pergunta não exige. Evite jargão, diminutivos excessivos, voz de bebê e elogios automáticos. "
            "Exemplos também precisam estar sustentados pelos trechos: não invente fatos, experiências "
            "ou recomendações para tornar a explicação divertida. Não diga que realizou uma experiência. "
            "A simplicidade não pode mudar o significado nem dispensar fontes ou proteções."
        ),
    },
}
