import re
import spacy
from typing import List


# spaCy 实体 → 我们系统里的 PII 类型
NER_TO_PII = {
    "PERSON": "NAME",
    "DATE": "DATE",
}

SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def ner_detect_pii(text: str) -> List[str]:
    """
    Semantic detector:
    返回这段文本里【可能需要 redaction 的 PII 类型】
    """
    nlp = get_nlp()
    doc = nlp(text)

    detected = set()

    for ent in doc.ents:
        if ent.label_ in NER_TO_PII:
            detected.add(NER_TO_PII[ent.label_])

    if SSN_PATTERN.search(text):
        detected.add("SSN")

    return list(detected)
