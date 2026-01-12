#!/usr/bin/env python3
"""测试说话人识别功能"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ingestion'))

from asr.diarize import assign_speakers, guess_first_speaker

def test_speaker_identification():
    """测试说话人识别功能"""
    
    # 测试用例
    test_cases = [
        {
            "name": "医生先问候",
            "segments": [
                {"text": "Hi, what can I help you?"},
                {"text": "Hey, I'm Jack Stuart."},
                {"text": "I think again, I'm having some code."},
                {"text": "I'm not headache anymore, but I'm continuing coughing."}
            ],
            "expected_first": "Doctor"
        },
        {
            "name": "患者先自我介绍", 
            "segments": [
                {"text": "Hi, I am Jack Stuart."},
                {"text": "I'm currently suffering from some painful diseases."},
                {"text": "Okay, let me take a look."}
            ],
            "expected_first": "Patient"
        },
        {
            "name": "医生专业问候",
            "segments": [
                {"text": "Good morning, what brings you in today?"},
                {"text": "I have been feeling sick."},
                {"text": "Can you describe your symptoms?"}
            ],
            "expected_first": "Doctor"
        },
        {
            "name": "患者直接描述症状",
            "segments": [
                {"text": "I feel terrible today."},
                {"text": "What seems to be the problem?"},
                {"text": "I have a headache and fever."}
            ],
            "expected_first": "Patient"
        }
    ]
    
    print("Testing Speaker Identification:")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("-" * 40)
        
        # 测试第一个说话人识别
        first_text = " ".join([seg["text"] for seg in test_case["segments"][:2]])
        predicted_first = guess_first_speaker(first_text)
        
        print(f"Input segments:")
        for j, seg in enumerate(test_case["segments"]):
            print(f"  {j+1}. {seg['text']}")
        
        print(f"\nFirst speaker prediction: {predicted_first}")
        print(f"Expected first speaker: {test_case['expected_first']}")
        print(f"✓ Correct" if predicted_first == test_case['expected_first'] else "✗ Incorrect")
        
        # 测试完整的说话人分配
        result = assign_speakers(test_case["segments"])
        print(f"\nComplete speaker assignment:")
        for seg in result:
            print(f"  {seg['speaker']}: {seg['text']}")
        
        print("=" * 40)

def test_specific_phrases():
    """测试特定短语的识别"""
    
    print("\n\nTesting Specific Phrases:")
    print("=" * 60)
    
    phrases = [
        ("Hi, what can I help you?", "Doctor"),
        ("I am Jack Stuart", "Patient"), 
        ("Good morning, what brings you in?", "Doctor"),
        ("I feel sick", "Patient"),
        ("Let me examine you", "Doctor"),
        ("My name is John", "Patient"),
        ("How can I help you today?", "Doctor"),
        ("I'm experiencing pain", "Patient")
    ]
    
    for phrase, expected in phrases:
        predicted = guess_first_speaker(phrase)
        status = "✓" if predicted == expected else "✗"
        print(f"{status} '{phrase}' -> {predicted} (expected: {expected})")

if __name__ == "__main__":
    test_speaker_identification()
    test_specific_phrases()