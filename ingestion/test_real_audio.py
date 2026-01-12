#!/usr/bin/env python3
"""
测试真实音频转录内容的处理
"""

from rag_system import RAGSystem

def test_real_audio_transcript():
    """测试真实的音频转录内容"""
    print("=== Testing Real Audio Transcript Processing ===")
    
    rag = RAGSystem()
    
    # 模拟真实的音频转录内容（基于你提供的实际转录）
    real_transcript = """
    Patient: Hi, what can I help you?
    Doctor: Hey, I'm John Smith.
    Patient: I think again, I'm having some cough.
    Doctor: I'm not having headache anymore, but I'm continuing coughing.
    """
    
    print("Processing real audio conversation...")
    print(f"Transcript: {real_transcript}")
    
    result = rag.process_conversation(real_transcript)
    
    print(f"\nResults:")
    print(f"Patient ID: {result['patient_id']}")
    print(f"Patient identified: {result['patient_identified']}")
    print(f"New medical info extracted: {len(result.get('new_medical_info', []))}")
    
    if result.get('new_medical_info'):
        print("\nNew medical information:")
        for info in result['new_medical_info']:
            print(f"  - {info['type']}: {info['content']}")
    
    print(f"\nTotal medical records now: {len(result['medical_records'])}")
    
    # 显示所有医疗记录（包括历史记录和新记录）
    print("\nAll medical records (including history):")
    for i, record in enumerate(result['medical_records']):
        source = record.get('metadata', {}).get('source', 'unknown') if isinstance(record.get('metadata'), dict) else 'unknown'
        print(f"  {i+1}. [{record['type']}] ({source}) {record['content'][:80]}...")
    
    return result

def test_another_conversation():
    """测试另一个对话，看看是否会累积记录"""
    print("\n=== Testing Another Conversation ===")
    
    rag = RAGSystem()
    
    # 另一个对话
    another_transcript = """
    Doctor: How are you feeling today?
    Patient: Hi, I'm John Smith. I'm still having some headache and now I feel dizzy too.
    Doctor: Are you taking any medication for that?
    Patient: Yes, I'm taking some pain medication, but it's not helping much.
    """
    
    print("Processing another conversation...")
    result = rag.process_conversation(another_transcript)
    
    print(f"\nResults:")
    print(f"Patient ID: {result['patient_id']}")
    print(f"New medical info extracted: {len(result.get('new_medical_info', []))}")
    
    if result.get('new_medical_info'):
        print("\nNew medical information:")
        for info in result['new_medical_info']:
            print(f"  - {info['type']}: {info['content']}")
    
    print(f"\nTotal medical records now: {len(result['medical_records'])}")
    
    return result

if __name__ == "__main__":
    # 测试真实音频转录
    test_real_audio_transcript()
    
    # 测试另一个对话
    test_another_conversation()