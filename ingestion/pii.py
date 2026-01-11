
import re
from typing import Tuple, List
import spacy

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
# DATE (强规则)
# ===============================
MONTH = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|" \
        r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"

DATE_PATTERNS = [
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",
    r"\b\d{4}/\d{1,2}/\d{1,2}\b",
    r"\b\d{4}-\d{1,2}-\d{1,2}\b",
    rf"\b{MONTH}\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s*\d{{4}})?\b",
]

DATE_REGEXES = [re.compile(p, re.IGNORECASE) for p in DATE_PATTERNS]

# ===============================
# SSN (强规则)
# ===============================
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


# ===============================
# 主入口
# ===============================
def redact_pii(text: str, allowed_types: List[str] = None) -> Tuple[str, List[str]]:
    """
    PII Redaction (Precision-first)

    - NAME: spaCy PERSON only
    - DATE: regex always-on
    - SSN: regex always-on
    """
    if allowed_types is None:
        allowed_types = []

    redacted = text
    found = []

    # ---------- DATE ----------
    for regex in DATE_REGEXES:
        if regex.search(redacted):
            redacted = regex.sub("[DATE]", redacted)
            found.append("DATE")

    # ---------- SSN ----------
    if SSN_PATTERN.search(redacted):
        redacted = SSN_PATTERN.sub("[SSN]", redacted)
        found.append("SSN")

    # ---------- NAME (spaCy only) ----------
    if "NAME" in allowed_types:
        try:
            nlp = get_nlp()
            doc = nlp(redacted)

            # 反向替换，避免 span index 失效
            for ent in reversed(doc.ents):
                if ent.label_ == "PERSON":
                    redacted = (
                        redacted[:ent.start_char]
                        + "[NAME]"
                        + redacted[ent.end_char:]
                    )
                    found.append("NAME")
        except Exception:
            pass

    return redacted, list(set(found))
