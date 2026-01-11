import re
from typing import Tuple, List

NAME_PATTERN = re.compile(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b")
DATE_PATTERN = re.compile(r"\b(\d{1,2}/\d{1,2}/\d{2,4})\b")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


def redact_pii(text: str) -> Tuple[str, List[str]]:
    redacted = text
    found = []

    if NAME_PATTERN.search(redacted):
        redacted = NAME_PATTERN.sub("[NAME]", redacted)
        found.append("NAME")

    if DATE_PATTERN.search(redacted):
        redacted = DATE_PATTERN.sub("[DATE]", redacted)
        found.append("DATE")

    if SSN_PATTERN.search(redacted):
        redacted = SSN_PATTERN.sub("[SSN]", redacted)
        found.append("SSN")

    return redacted, found
