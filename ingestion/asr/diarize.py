from typing import List, Dict

DOCTOR_TERMS = {
    "doctor", "dr", "physician", "nurse", "provider"
}

PATIENT_TERMS = {
    "patient", "i feel", "i have", "my pain", "i'm experiencing"
}

MEDICAL_QUESTIONS = {
    "what should i", "how do i", "when should i", "can i take", "is it normal"
}

def is_question(text: str) -> bool:
    text = text.strip().lower()
    return text.endswith("?") or text.startswith(("what", "how", "why", "when", "where", "can", "do", "did", "are", "is", "should"))

def contains_doctor_reference(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in DOCTOR_TERMS)

def contains_patient_indicators(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in PATIENT_TERMS)

def contains_medical_question(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in MEDICAL_QUESTIONS)

def guess_first_speaker(text: str) -> str:
    """
    Enhanced Phase 1 role inference heuristic:
    - Patient indicators (I feel, I have, etc.) -> Patient
    - Medical questions from patient -> Patient  
    - Professional questions/statements -> Doctor
    - Questions referencing doctor -> Patient
    - Default -> Patient (conservative approach)
    """
    if contains_patient_indicators(text):
        return "Patient"
    
    if contains_medical_question(text):
        return "Patient"
    
    if is_question(text):
        if contains_doctor_reference(text):
            return "Patient"
        # Professional medical questions likely from doctor
        return "Doctor"
    
    # Default to patient for safety
    return "Patient"


def assign_speakers(segments: List[Dict]) -> List[Dict]:
    if not segments:
        return []

    # Analyze first few segments to get better initial speaker
    first_texts = [seg["text"] for seg in segments[:3]]
    combined_start = " ".join(first_texts).lower()
    
    current_speaker = guess_first_speaker(combined_start)

    transcript = []
    for i, seg in enumerate(segments):
        # Re-evaluate speaker for certain key phrases
        text_lower = seg["text"].lower()
        
        # Strong patient indicators
        if any(indicator in text_lower for indicator in PATIENT_TERMS):
            current_speaker = "Patient"
        # Strong doctor indicators (professional language)
        elif any(phrase in text_lower for phrase in ["let me examine", "i recommend", "the diagnosis", "your symptoms indicate"]):
            current_speaker = "Doctor"
        
        transcript.append({
            "speaker": current_speaker,
            "text": seg["text"]
        })
        
        # Alternate speakers, but allow override by strong indicators
        if i < len(segments) - 1:  # Don't alternate after last segment
            current_speaker = "Doctor" if current_speaker == "Patient" else "Patient"

    return transcript
