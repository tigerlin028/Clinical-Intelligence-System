from faster_whisper import WhisperModel
from typing import List, Dict

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading Whisper model...")
        _model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )
        print("Whisper model loaded.")
    return _model


def transcribe_audio(file_path: str) -> List[Dict]:
    model = get_model()
    segments, _ = model.transcribe(file_path)

    results = []
    for seg in segments:
        results.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip()
        })
    return results
