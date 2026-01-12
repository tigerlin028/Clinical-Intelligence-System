from faster_whisper import WhisperModel
from typing import List, Dict
import time
import os

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading Whisper model...")
        
        # 尝试多种模型配置，从最简单的开始
        model_configs = [
            {"model_size_or_path": "tiny", "device": "cpu", "compute_type": "int8"},
            {"model_size_or_path": "base", "device": "cpu", "compute_type": "int8"},
        ]
        
        for i, config in enumerate(model_configs):
            try:
                print(f"Trying model config {i+1}: {config['model_size_or_path']}")
                _model = WhisperModel(**config)
                print(f"Successfully loaded {config['model_size_or_path']} model.")
                break
            except Exception as e:
                print(f"Failed to load {config['model_size_or_path']} model: {e}")
                if i < len(model_configs) - 1:
                    print("Retrying with different model...")
                    time.sleep(2)
                else:
                    print("All model configs failed, using fallback...")
                    # 最后的fallback - 使用最小的模型
                    try:
                        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
                        print("Fallback tiny model loaded.")
                    except Exception as fallback_error:
                        print(f"Even fallback failed: {fallback_error}")
                        raise Exception("Unable to load any Whisper model")
    
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
