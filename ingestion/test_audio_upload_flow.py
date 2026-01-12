#!/usr/bin/env python3
"""
测试完整的音频上传流程
"""

from rag_system import RAGSystem
from database import PatientDatabase, MedicalRecordsDatabase

def simulate_audio_upload_processing():
    """模拟音频上传处理的完整流程"""
    print("=== Simulating Complete Audio Upload Flow ===")
    
    # 模拟音频转录结果（这是从音频文件转录出来的实际内容）
    # 基于你提供的真实转录内容
    simulated_transcript_segments = [
        {"speaker": "Patient", "text": "Hi, what can I help you?"},
        {"speaker": "Doctor", "text": "Hey, I'm John Smith."},
        {"speaker": "Patient", "text": "I think again, I'm having some cough."},
        {"speaker": "Doctor", "text": "I'm not having headache anymore, but I'm continuing coughing."}
    ]
    
    print("Simulated transcript from audio:")
    for seg in simulated_transcript_segments:
        print(f"  {seg['speaker']}: {seg['text']}")
    
    # 合并完整转录文本用于RAG处理（模拟main.py中的逻辑）
    full_text = " ".join([seg["text"] for seg in simulated_transcript_segments])
    print(f"\nFull text for RAG processing: {full_text}")
    
    # RAG系统处理
    rag_system = RAGSystem()
    print("\nStarting RAG processing...")
    rag_result = rag_system.process_conversation(full_text)
    
    # 模拟PII脱敏处理
    redacted_transcript = []
    for seg in simulated_transcript_segments:
        # 简单的脱敏处理（实际会更复杂）
        redacted_text = seg["text"].replace("John Smith", "[NAME]")
        redacted_transcript.append({
            "speaker": seg["speaker"],
            "text": redacted_text
        })
    
    print("\nRedacted transcript:")
    for seg in redacted_transcript:
        print(f"  {seg['speaker']}: {seg['text']}")
    
    # 构建响应（模拟API响应）
    response = {
        "transcript": redacted_transcript,
        "redaction_summary": ["NAME"],
        "detected_entity_types": ["PERSON"],
        "processing_note": "Phase 1: Audio transcription with speaker identification, PII redaction, and medical record retrieval",
        "segments_count": len(simulated_transcript_segments),
        "patient_identified": rag_result["patient_identified"],
        "patient_id": rag_result["patient_id"],
        "medical_records": rag_result["medical_records"],
        "extracted_patient_info": rag_result["extracted_info"]
    }
    
    print(f"\n=== Processing Results ===")
    print(f"Patient Identified: {response['patient_identified']}")
    print(f"Patient ID: {response['patient_id']}")
    print(f"Total Medical Records: {len(response['medical_records'])}")
    print(f"New Medical Info: {len(rag_result.get('new_medical_info', []))}")
    
    if rag_result.get('new_medical_info'):
        print("\nNew medical information extracted from audio:")
        for info in rag_result['new_medical_info']:
            print(f"  - {info['type']}: {info['content']}")
    
    print("\nAll medical records (history + new):")
    for i, record in enumerate(response['medical_records']):
        source = "unknown"
        if isinstance(record.get('metadata'), dict):
            source = record['metadata'].get('source', 'unknown')
        print(f"  {i+1}. [{record['type']}] ({source}) {record['content'][:60]}...")
    
    return response

def check_database_state():
    """检查数据库当前状态"""
    print("\n=== Current Database State ===")
    
    medical_db = MedicalRecordsDatabase()
    patient_db = PatientDatabase()
    
    # 获取John Smith的记录
    patient_id = patient_db.find_patient(name="John Smith", ssn="123-45-6789", dob="1985-03-15")
    if patient_id:
        records = medical_db.get_patient_records(patient_id)
        print(f"Patient {patient_id} has {len(records)} medical records:")
        
        for i, record in enumerate(records):
            source = "unknown"
            if isinstance(record.get('metadata'), dict):
                source = record['metadata'].get('source', 'unknown')
            print(f"  {i+1}. [{record['type']}] ({source}) - {record['date']}")
            print(f"      {record['content'][:80]}...")
    else:
        print("Patient not found in database")

if __name__ == "__main__":
    # 检查处理前的数据库状态
    print("Before processing:")
    check_database_state()
    
    # 模拟音频上传处理
    result = simulate_audio_upload_processing()
    
    # 检查处理后的数据库状态
    print("\nAfter processing:")
    check_database_state()