#!/usr/bin/env python3
"""
本地测试脚本 - 验证所有功能是否正常
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """测试所有导入是否正常"""
    try:
        from main import app
        from pii import redact_pii
        from pii_ner import ner_detect_pii
        from asr.transcribe import transcribe_audio
        from asr.diarize import assign_speakers
        print("✅ 所有导入正常")
        return True
    except Exception as e:
        print(f"❌ 导入错误: {e}")
        return False

def test_pii_redaction():
    """测试 PII 脱敏功能"""
    try:
        from pii import redact_pii
        from pii_ner import ner_detect_pii
        
        # 测试文本
        test_text = "My name is John Smith and my SSN is 123-45-6789. I was born on 01/15/1990."
        
        # 检测 PII 类型
        detected_types = ner_detect_pii(test_text)
        print(f"检测到的 PII 类型: {detected_types}")
        
        # 执行脱敏
        redacted_text, entities = redact_pii(test_text, allowed_types=detected_types)
        print(f"原文: {test_text}")
        print(f"脱敏后: {redacted_text}")
        print(f"脱敏实体: {entities}")
        
        # 验证脱敏是否生效
        assert "123-45-6789" not in redacted_text, "SSN 应该被脱敏"
        assert "01/15/1990" not in redacted_text, "日期应该被脱敏"
        print("✅ PII 脱敏功能正常")
        return True
    except Exception as e:
        print(f"❌ PII 脱敏测试失败: {e}")
        return False

def test_speaker_assignment():
    """测试说话人识别"""
    try:
        from asr.diarize import assign_speakers
        
        # 模拟转录片段
        segments = [
            {"text": "Hello, I'm having chest pain."},
            {"text": "When did this pain start?"},
            {"text": "It started this morning around 8 AM."},
            {"text": "Can you describe the pain?"}
        ]
        
        transcript = assign_speakers(segments)
        print("说话人识别结果:")
        for seg in transcript:
            print(f"  {seg['speaker']}: {seg['text']}")
        
        print("✅ 说话人识别功能正常")
        return True
    except Exception as e:
        print(f"❌ 说话人识别测试失败: {e}")
        return False

def main():
    print("🧪 开始本地功能测试...\n")
    
    tests = [
        ("导入测试", test_imports),
        ("PII 脱敏测试", test_pii_redaction),
        ("说话人识别测试", test_speaker_assignment),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        result = test_func()
        results.append(result)
    
    print(f"\n📊 测试结果: {sum(results)}/{len(results)} 通过")
    
    if all(results):
        print("🎉 所有测试通过！代码可以部署。")
        print("\n💡 下一步:")
        print("1. 更新 deploy.sh 中的 PROJECT_ID")
        print("2. 运行: ./deploy.sh")
        print("3. 或者本地开发: uvicorn main:app --reload")
    else:
        print("⚠️ 有测试失败，请检查代码。")

if __name__ == "__main__":
    main()