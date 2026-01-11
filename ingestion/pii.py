# ingestion/pii.py

import re
from typing import Tuple, List

# ===============================
# Stopwords (用于 NAME 过滤)
# ===============================
STOPWORDS = {
    "was", "is", "are", "were", "be", "been",
    "on", "in", "at", "of", "for", "with",
    "born", "and", "or", "the", "a", "an",
    "doctor", "dr", "patient", "name", "names"
}

# ===============================
# NAME (2–3 连续词，大小写无关)
# ===============================
NAME_PATTERN = re.compile(
    r"\b([A-Za-z]+(?:\s+[A-Za-z]+){1,2})\b"
)

def is_valid_name_span(span: str) -> bool:
    """
    判断一个 span 是否可能是人名：
    - 至少 2 个词
    - 不包含 stopwords
    """
    tokens = span.lower().split()
    if len(tokens) < 2:
        return False
    return all(tok not in STOPWORDS for tok in tokens)

def redact_names(text: str) -> Tuple[str, bool]:
    """
    安全替换 NAME：
    - 收集所有合法 span
    - 按 span 长度从大到小排序
    - 只替换最长且不重叠的 span
    """
    matches = []

    for match in NAME_PATTERN.finditer(text):
        span = match.group(1)
        start, end = match.span(1)

        if is_valid_name_span(span):
            matches.append((start, end, span))

    if not matches:
        return text, False

    # 最长 span 优先
    matches.sort(key=lambda x: x[1] - x[0], reverse=True)

    redacted = text
    replaced_ranges = []

    for start, end, span in matches:
        # 检查是否与已替换区间重叠
        if any(not (end <= s or start >= e) for s, e in replaced_ranges):
            continue

        redacted = redacted[:start] + "[NAME]" + redacted[end:]
        replaced_ranges.append((start, start + len("[NAME]")))

    return redacted, True

# ===============================
# DATE (强规则，全覆盖)
# ===============================
MONTH = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|" \
        r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"

DATE_PATTERNS = [
    # 02/05/1998 or 02/05/98
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",

    # 02-05-1998
    r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",

    # 1998/02/05
    r"\b\d{4}/\d{1,2}/\d{1,2}\b",

    # 1998-02-05
    r"\b\d{4}-\d{1,2}-\d{1,2}\b",

    # Feb 5th 1998 / Feb 5, 1998 / Feb 5
    rf"\b{MONTH}\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s*\d{{4}})?\b",
]

DATE_REGEXES = [re.compile(p, re.IGNORECASE) for p in DATE_PATTERNS]

# ===============================
# SSN
# ===============================
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

# ===============================
# 主入口
# ===============================
def redact_pii(text: str, allowed_types: List[str] = None) -> Tuple[str, List[str]]:
    """
    PII Redaction 主逻辑

    - NAME: gated + span-safe
    - DATE: always-on regex
    - SSN: always-on regex
    """
    if allowed_types is None:
        allowed_types = []

    redacted = text
    found = []

    # ---------- DATE（先做，避免被 NAME 破坏） ----------
    for regex in DATE_REGEXES:
        if regex.search(redacted):
            redacted = regex.sub("[DATE]", redacted)
            found.append("DATE")

    # ---------- SSN ----------
    if SSN_PATTERN.search(redacted):
        redacted = SSN_PATTERN.sub("[SSN]", redacted)
        found.append("SSN")

    # ---------- NAME（最后，且 gated） ----------
    if "NAME" in allowed_types:
        redacted, did_replace = redact_names(redacted)
        if did_replace:
            found.append("NAME")

    return redacted, list(set(found))
