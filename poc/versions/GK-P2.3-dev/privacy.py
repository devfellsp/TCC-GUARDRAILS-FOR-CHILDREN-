"""Minimizacao de logs; deteccao adicional nao substitui a omissao de texto livre."""
import copy
import re

OMITTED = "[texto omitido pelo modo de privacidade]"
PATTERNS = (
    r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b",
    r"(?<!\w)(?:\+?55\s*)?\(?\d{2}\)?[\s.-]*\d{4,5}[\s.-]*\d{4}(?!\w)",
    r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)",
    r"\b(?:meu nome(?: completo)? [ée]|me chamo|moro (?:na|no|em)|meu endere[cç]o [ée]|minha escola [ée])\s+\S+",
)


def contains_private_data(text):
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in PATTERNS)


def log_record(record, synthetic=False):
    """Apenas o executor de casos explicitamente ficticios habilita logs integrais."""
    saved = copy.deepcopy(record)
    saved["logging_mode"] = "synthetic" if synthetic else "minimized"
    if synthetic:
        return saved
    saved["question"] = OMITTED
    if saved.get("final_origin") == "generation":
        saved["answer"] = OMITTED
    if saved.get("generated"):
        saved["generated"]["answer"] = OMITTED
    if saved.get("draft"):
        saved["draft"] = OMITTED
    for key in ("input_guard", "output_guard", "grounding_guard"):
        if saved.get(key):
            saved[key]["reason"] = OMITTED
            for verdict in saved[key].get("claims", []):
                verdict["reason"] = OMITTED
    # Conteudo curricular permanece no snapshot; logs comuns guardam apenas IDs/escores.
    for chunk in saved.get("retrieved", []):
        chunk.pop("text", None)
    return saved
