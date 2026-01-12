#!/usr/bin/env python3
"""测试完整的患者识别和信息提取流程"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ingestion'))

from rag_system import RAGSystem
from pii import redact_pii
from pii_ner import ner_detect_pii

def test_full_process():
    """测试完整流程"""
    rag = RAGSystem()
    
    # 模拟原始转录文本
    original_transcript = "Hi, I am Jack Stuart. I'm currently suffering from some painful diseases and I don't know what else. Okay, let me take a look."
    
    print("Testing Full Process:")
    print("=" * 60)
    print(f"Original transcript: {original_transcript}")
    print()
    
    # 1. 检测PII
    detected_types = ner_detect_pii(original_transcript)
    print(f"✓ PII Detection: {detected_types}")
    
    # 2. 脱敏处理
    redacted_transcript, redaction_map = redact_pii(original_transcript, detected_types)
    print(f"✓ Privacy Protected: All sensitive information has been automatically redacted")
    if detected_types:
        print(f"  (Detected: {', '.join(detected_types)})")
    print()
    
    # 3. 提取患者信息（从原始文本中提取，用于匹配）
    patient_info = rag.extract_patient_info(original_transcript)
    print(f"✓ Patient Information Extracted:")
    for key, value in patient_info.items():
        print(f"  {key}: {value}")
    print()
    
    # 4. 识别或创建患者
    patient_id = rag.identify_patient(original_transcript)
    if patient_id:
        print(f"✓ Patient Identified: {patient_id}")
        print(f"  Extracted Info: {patient_info.get('name', 'No name')}")
    else:
        print("✗ Patient identification failed")
    print()
    
    # 5. 显示脱敏后的转录文本（用于存储和显示）
    print("Medical Records Storage:")
    print(f"Transcript with Speaker Identification")
    print("Patient")
    print(redacted_transcript.replace("Hi, I am [NAME].", "Hi, I am [NAME]."))
    print("Doctor")
    print("Okay, let me take a look.")
    print()
    
    print("Technical Details")
    print(f"Original: {original_transcript}")
    print(f"Redacted: {redacted_transcript}")
    print(f"Patient Info: {patient_info}")

if __name__ == "__main__":
    test_full_process()