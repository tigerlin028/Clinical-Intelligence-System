#!/usr/bin/env python3
"""测试姓名提取功能"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ingestion'))

from rag_system import RAGSystem

def test_name_extraction():
    """测试姓名提取功能"""
    rag = RAGSystem()
    
    # 测试用例
    test_cases = [
        "Hi, I am Jack Stuart. I'm currently suffering from some painful diseases and I don't know what else.",
        "My name is John Smith and I have a headache.",
        "I'm Mary Johnson. I'm feeling sick today.",
        "This is David Wilson speaking.",
        "Hi, I am currently suffering from pain.",  # 这个应该不提取姓名
    ]
    
    print("Testing name extraction:")
    print("=" * 50)
    
    for i, transcript in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {transcript}")
        
        patient_info = rag.extract_patient_info(transcript)
        extracted_name = patient_info.get('name', 'No name extracted')
        
        print(f"Extracted Name: {extracted_name}")
        print("-" * 30)

if __name__ == "__main__":
    test_name_extraction()