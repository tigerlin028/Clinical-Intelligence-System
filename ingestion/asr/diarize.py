from typing import List, Dict

DOCTOR_TERMS = {
    "doctor", "dr", "physician", "nurse", "provider"
}

PATIENT_TERMS = {
    "patient", "i feel", "i have", "my pain", "i'm experiencing", "i am", "my name is"
}

MEDICAL_QUESTIONS = {
    "what should i", "how do i", "when should i", "can i take", "is it normal"
}

# 医生常用的开场问候语和专业用语
DOCTOR_GREETINGS = {
    "what can i help you", "how can i help", "what brings you", "what seems to be", 
    "how are you feeling", "what's the problem", "what's bothering you",
    "hi, what can i help", "hello, what can i help", "good morning, what can i help",
    "let me examine", "let me take a look", "let me check"
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

def is_doctor_greeting(text: str) -> bool:
    """检查是否是医生的开场问候语"""
    lowered = text.lower()
    return any(greeting in lowered for greeting in DOCTOR_GREETINGS)

def guess_first_speaker(text: str) -> str:
    """
    改进的说话人识别逻辑：
    1. 如果是医生常用的问候语（如"what can I help you"），则是医生
    2. 如果包含患者自我介绍（如"I am [name]"），则是患者  
    3. 如果包含患者症状描述，则是患者
    4. 如果是问句但没有医生相关词汇，且像是服务性问候，则是医生
    5. 默认为患者（保守方法）
    """
    lowered = text.lower()
    
    # 1. 检查医生开场问候语 - 优先级最高
    if is_doctor_greeting(text):
        return "Doctor"
    
    # 2. 检查患者自我介绍和症状描述 - 优先级第二
    if contains_patient_indicators(text):
        return "Patient"
    
    # 3. 检查医疗相关问题（患者问的）
    if contains_medical_question(text):
        return "Patient"
    
    # 4. 如果是问句的进一步判断
    if is_question(text):
        # 如果问句中提到医生，通常是患者在问
        if contains_doctor_reference(text):
            return "Patient"
        # 如果是服务性问候（如"Hi, what can I help you?"），通常是医生
        if any(phrase in lowered for phrase in ["what can i help", "how can i help", "what brings you", "what seems to be"]):
            return "Doctor"
        # 其他问句，默认为医生（因为医生通常先问诊）
        return "Doctor"
    
    # 5. 检查是否包含"I feel"等患者症状描述
    if any(phrase in lowered for phrase in ["i feel", "i have", "i'm feeling"]):
        return "Patient"
    
    # 6. 默认为患者
    return "Patient"


def assign_speakers(segments: List[Dict]) -> List[Dict]:
    if not segments:
        return []

    # 分析前几个片段来确定初始说话人
    first_texts = [seg["text"] for seg in segments[:3]]
    combined_start = " ".join(first_texts)
    
    # 使用改进的逻辑确定第一个说话人
    current_speaker = guess_first_speaker(combined_start)

    transcript = []
    for i, seg in enumerate(segments):
        text_lower = seg["text"].lower()
        
        # 强患者指标 - 强制切换到患者
        if any(indicator in text_lower for indicator in PATIENT_TERMS):
            current_speaker = "Patient"
        # 强医生指标 - 强制切换到医生
        elif any(phrase in text_lower for phrase in ["let me examine", "i recommend", "the diagnosis", "your symptoms indicate", "okay, let me take a look"]):
            current_speaker = "Doctor"
        # 医生问候语 - 强制切换到医生
        elif is_doctor_greeting(seg["text"]):
            current_speaker = "Doctor"
        
        transcript.append({
            "speaker": current_speaker,
            "text": seg["text"]
        })
        
        # 交替说话人，但允许被强指标覆盖
        if i < len(segments) - 1:  # 不在最后一个片段后交替
            current_speaker = "Doctor" if current_speaker == "Patient" else "Patient"

    return transcript
