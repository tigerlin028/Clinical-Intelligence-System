#!/usr/bin/env python3
"""
测试新功能：医疗信息提取和重复记录避免
"""

from rag_system import RAGSystem

def test_medical_info_extraction():
    """测试医疗信息提取功能"""
    print("=== Testing Medical Information Extraction ===")
    
    rag = RAGSystem()
    
    # 测试包含症状的对话
    test_transcript = """
    Doctor: Hi, what can I help you?
    Patient: Hi, I'm John Smith. I'm having a headache and feeling dizzy.
    Doctor: Okay, what's your date of birth?
    Patient: It's 1985-03-15.
    Doctor: And your SSN?
    Patient: 123-45-6789.
    Doctor: Are you taking any medications?
    Patient: Yes, I'm taking some pain medication for the headache.
    """
    
    print("Processing conversation...")
    result = rag.process_conversation(test_transcript)
    
    print(f"Patient ID: {result['patient_id']}")
    print(f"Patient identified: {result['patient_identified']}")
    print(f"New medical info extracted: {len(result.get('new_medical_info', []))}")
    
    for info in result.get('new_medical_info', []):
        print(f"  - {info['type']}: {info['content']}")
    
    print(f"Total medical records now: {len(result['medical_records'])}")
    
    # 显示所有医疗记录
    print("\nAll medical records:")
    for i, record in enumerate(result['medical_records']):
        print(f"  {i+1}. [{record['type']}] {record['content']}")
    
    return result

def test_duplicate_prevention():
    """测试重复记录防止功能"""
    print("\n=== Testing Duplicate Prevention ===")
    
    rag = RAGSystem()
    
    # 再次处理相同的对话，应该不会产生重复记录
    same_transcript = """
    Doctor: Hi, what can I help you?
    Patient: Hi, I'm John Smith. I'm having a headache and feeling dizzy.
    Doctor: Okay, what's your date of birth?
    Patient: It's 1985-03-15.
    """
    
    print("Processing same conversation again...")
    result = rag.process_conversation(same_transcript)
    
    print(f"New medical info extracted (should be 0 or minimal): {len(result.get('new_medical_info', []))}")
    print(f"Total medical records: {len(result['medical_records'])}")

if __name__ == "__main__":
    test_medical_info_extraction()
    test_duplicate_prevention()