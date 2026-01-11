import re
from typing import Tuple, List

NAME_PATTERN = re.compile(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b")
DATE_PATTERN = re.compile(r"\b(\d{1,2}/\d{1,2}/\d{2,4})\b")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

def redact_pii(text: str, allowed_types: List[str] = None) -> Tuple[str, List[str]]:
    if allowed_types is None:
        allowed_types = ["NAME", "SSN", "DATE"]

    redacted = text
    found = []

    if "NAME" in allowed_types and NAME_PATTERN.search(redacted):
        redacted = NAME_PATTERN.sub("[NAME]", redacted)
        found.append("NAME")

    if "DATE" in allowed_types and DATE_PATTERN.search(redacted):
        redacted = DATE_PATTERN.sub("[DATE]", redacted)
        found.append("DATE")

    if "SSN" in allowed_types and SSN_PATTERN.search(redacted):
        redacted = SSN_PATTERN.sub("[SSN]", redacted)
        found.append("SSN")

    return redacted, found
