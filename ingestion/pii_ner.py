import spacy
from typing import List

# 只用 spaCy 判断“有没有可能是人名”
NER_TO_PII = {
    "PERSON": "NAME",
}

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def ner_detect_pii(text: str) -> List[str]:
    """
    Semantic detector:
    - 只负责 NAME
    - DATE / SSN 不在这里处理
    """
    detected = set()

    nlp = get_nlp()
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ in NER_TO_PII:
            detected.add("NAME")

    return list(detected)
