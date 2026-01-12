from typing import List, Dict

DOCTOR_TERMS = {"doctor", "dr", "physician"}

# 连续说话阈值（秒）
SAME_SPEAKER_MAX_GAP = 1.0  # 你可以调：0.7 ~ 1.5 都合理


def is_question(text: str) -> bool:
    text = text.strip().lower()
    return (
        text.endswith("?")
        or text.startswith(
            ("what", "how", "why", "when", "where", "can", "do", "did", "are", "is")
        )
    )


def contains_doctor_reference(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in DOCTOR_TERMS)


def guess_first_speaker(text: str) -> str:
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

    last_end_time = segments[0]["end"]

    transcript.append({
        "speaker": current_speaker,
        "text": segments[0]["text"]
    })

    for seg in segments[1:]:
        gap = seg["start"] - last_end_time

        # 核心逻辑：时间间隔很短 → 同一 speaker
        if gap > SAME_SPEAKER_MAX_GAP:
            current_speaker = "Doctor" if current_speaker == "Patient" else "Patient"

        transcript.append({
            "speaker": current_speaker,
            "text": seg["text"]
        })

        last_end_time = seg["end"]

    return transcript
