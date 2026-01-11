# ingestion/pii.py

import re
from typing import Tuple, List

# ---------------- STOPWORDS ----------------
STOPWORDS = {
    "was", "is", "are", "were", "be", "been",
    "on", "in", "at", "of", "for", "with",
    "born", "and", "or", "the", "a", "an",
}

# ---------------- NAME ----------------
# 只匹配 2–3 个连续英文词
NAME_PATTERN = re.compile(
    r"\b([A-Za-z]+(?:\s+[A-Za-z]+){1,2})\b"
)

# ---------------- DATE ----------------
MONTH = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"

DATE_PATTERNS = [
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",
    r"\b\d{4}/\d{1,2}/\d{1,2}\b",
    r"\b\d{4}-\d{1,2}-\d{1,2}\b",
    rf"\b{MONTH}\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s*\d{{4}})?\b",
]

DATE_REGEXES = [re.compile(p, re.IGNORECASE) for p in DATE_PATTERNS]

# ---------------- SSN ----------------
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


def is_valid_name_span(span: str) -> bool:
    """
    判断一个 span 是否可能是姓名
    """
    tokens = span.lower().split()
    if len(tokens) < 2:
        return False
    return all(tok not in STOPWORDS for tok in tokens)


def redact_pii(text: str, allowed_types: List[str] = None) -> Tuple[str, List[str]]:
    if allowed_types is None:
        allowed_types = []

    redacted = text
    found = []

    # ---------- DATE FIRST（防止被 NAME 破坏） ----------
    for regex in DATE_REGEXES:
        if regex.search(redacted):
            redacted = regex.sub("[DATE]", redacted)
            found.append("DATE")

    # ---------- SSN ----------
    if SSN_PATTERN.search(redacted):
        redacted = SSN_PATTERN.sub("[SSN]", redacted)
        found.append("SSN")

    # ---------- NAME（最后 & gated & 校验） ----------
    if "NAME" in allowed_types:
        def _name_sub(match):
            span = match.group(1)
            if is_valid_name_span(span):
                found.append("NAME")
                return "[NAME]"
            return span  # 不替换

        redacted = NAME_PATTERN.sub(_name_sub, redacted)

    return redacted, list(set(found))
