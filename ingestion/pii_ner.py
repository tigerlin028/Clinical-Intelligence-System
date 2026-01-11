import spacy
from typing import List

# ===============================
# spaCy lazy loader
# ===============================
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


# ===============================
# NAME fallback triggers
# ===============================
NAME_TRIGGERS = {
    "doctor", "dr", "patient",
    "name", "names",
    "mr", "ms", "mrs"
}

def should_try_name_fallback(text: str) -> bool:
    """
    Rule-based fallback trigger:
    用于 spaCy 未检测到 PERSON，但句子形态明显在提名字的情况
    """
    lowered = text.lower()
    return any(trigger in lowered for trigger in NAME_TRIGGERS)


# ===============================
# Main semantic detector
# ===============================
def ner_detect_pii(text: str) -> List[str]:
    """
    Determine which PII types are worth attempting.

    - NAME:
        - spaCy detects PERSON
        - OR fallback trigger fires
    - DATE / SSN:
        - Not handled here (always-on in regex layer)
    """
    detected = set()

    # ---------- spaCy semantic detection ----------
    try:
        nlp = get_nlp()
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                detected.add("NAME")
                break
    except Exception:
        # spaCy failure should never block redaction
        pass

    # ---------- fallback trigger ----------
    if "NAME" not in detected and should_try_name_fallback(text):
        detected.add("NAME")

    return list(detected)
