from typing import List
import re
from transformers import pipeline

# Regex for always-on PII
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

# Lazy-loaded pipeline
_ner_pipeline = None

def get_ner_pipeline():
    global _ner_pipeline
    if _ner_pipeline is None:
        _ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple"
        )
    return _ner_pipeline

def bert_detect_pii(text: str) -> List[str]:
    """
    High-recall PII detector using Transformer NER + regex fallback
    """
    detected = set()

    # ① Transformer NER (NAME, DATE)
    ner = get_ner_pipeline()
    results = ner(text)

    for ent in results:
        if ent["entity_group"] == "PER":
            detected.add("NAME")
        elif ent["entity_group"] == "DATE":
            detected.add("DATE")

    # ② Regex-only PII (always-on)
    if SSN_PATTERN.search(text):
        detected.add("SSN")

    return list(detected)
