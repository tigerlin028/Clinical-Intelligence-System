from typing import List, Dict

DOCTOR_TERMS = {
    "doctor", "dr", "physician"
}

def is_question(text: str) -> bool:
    text = text.strip().lower()
    return text.endswith("?") or text.startswith(("what", "how", "why", "when", "where", "can", "do", "did", "are", "is"))

def contains_doctor_reference(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in DOCTOR_TERMS)


def guess_first_speaker(text: str) -> str:
    """
    Phase 1 role inference heuristic:
    - Question + no doctor reference -> Doctor
    - Question + doctor reference    -> Patient
    - Otherwise                      -> Patient
    """
    if is_question(text):
        if contains_doctor_reference(text):
            return "Patient"
        return "Doctor"
    return "Patient"


def assign_speakers(segments: List[Dict]) -> List[Dict]:
    if not segments:
        return []

    current_speaker = guess_first_speaker(segments[0]["text"])

    transcript = []
    for seg in segments:
        transcript.append({
            "speaker": current_speaker,
            "text": seg["text"]
        })
        current_speaker = "Doctor" if current_speaker == "Patient" else "Patient"

    return transcript
