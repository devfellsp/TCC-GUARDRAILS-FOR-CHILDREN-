"""Barreira lexical conservadora; não é prova de implicação semântica."""
import re
import unicodedata

# Conectivos, pronomes e verbos auxiliares permitem frases naturais. Substantivos,
# números e verbos de processos concretos precisam de âncora na evidência citada.
FUNCTION_WORDS = set("""
a ao aos as o os um uma uns umas de do da dos das em no na nos nas por pelo pela
pelos pelas para com sem e ou mas se que como quando onde porque pois assim tambem
ja so mais menos muito muita muitos muitas pouco pouca poucos poucas cada esse essa
esses essas este esta estes estas isso isto aquele aquela aqueles aquelas aqui ali la
seu sua seus suas ele ela eles elas nos voce voces eu meu minha meus minhas outro
outra outros outras mesmo mesma mesmos mesmas todo toda todos todas qual quais
quem quanto quantos tanto quanto nao nem sim entre sobre ate desde durante depois
antes alem ainda apenas principalmente segundo conforme exemplo texto fonte
e sao era eram ser sendo sido estar esta estao estava estavam tem tinha tinham ter
ha havia podem pode poderia poderiam devem deve precisa precisam permite permitem
fica ficam ficar ficam faz fazem fazer feito feita feitos feitas ajuda ajudam
ajudar ajudou usado usada usados usadas usa usam usar chamado chamada chamados
chamadas chama chamam significa significam dizer diz dizem seja sejam trata
tratar refere referem vive vivem viver passou passaram torna tornam oferece oferecem oferecer
enquanto tipo tipos nome nomes portanto entao dessa desse dessas desses deste desta destes destas
""".split())


def tokens(text):
    normalized = unicodedata.normalize("NFKD", text.lower())
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    return re.findall(r"[a-z]+|\d+(?:[.,]\d+)*", normalized)


def unanchored_words(text, quotes):
    evidence = set(tokens(" ".join(quotes)))
    # Prefixo de cinco letras acomoda flexões comuns sem dicionário externo.
    stems = {t[:5] for t in evidence if len(t) >= 5 and t.isalpha()}
    return sorted({word for word in tokens(text) if len(word) > 2 or word.isdigit()
                   if word not in FUNCTION_WORDS and word not in evidence
                   and not (len(word) >= 5 and word.isalpha() and word[:5] in stems)})
