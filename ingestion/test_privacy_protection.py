#!/usr/bin/env python3
"""
隐私保护功能测试脚本
测试PII脱敏在医疗记录存储中的效果
"""

from rag_system import RAGSystem
from database import init_sample_data
import json

def test_privacy_protection():
    """测试隐私保护功能"""
    print("🔒 测试隐私保护功能...")
    print("=" * 60)
    
    # 初始化系统
    init_sample_data()
    rag = RAGSystem()
    
    # 测试用的对话文本（包含PII）
    test_conversations = [
        {
            "name": "包含姓名的症状报告",
            "transcript": "Hi, I'm John Smith. I'm having a headache and feeling dizzy."
        },
        {
            "name": "包含姓名的药物信息",
            "transcript": "Yes, I'm John Smith, I'm taking some pain medication for the headache."
        },
        {
            "name": "结构化对话格式",
            "transcript": """Patient: Hi, I'm John Smith. I'm having a stomachache.
Doctor: I see, John. Let me prescribe something for you."""
        }
    ]
    
    for i, test_case in enumerate(test_conversations, 1):
        print(f"\n📋 测试案例 {i}: {test_case['name']}")
        print("-" * 40)
        print(f"原始文本: {test_case['transcript']}")
        
        # 处理对话
        result = rag.process_conversation(test_case['transcript'])
        
        if result['patient_identified']:
            print(f"✅ 患者识别成功: {result['patient_id']}")
            
            # 检查新提取的医疗信息
            if result['new_medical_info']:
                print(f"📝 提取到 {len(result['new_medical_info'])} 条新医疗信息:")
                for info in result['new_medical_info']:
                    print(f"   类型: {info['type']}")
                    print(f"   内容: {info['content']}")
                    
                    # 检查是否包含原始姓名
                    if "John Smith" in info['content']:
                        print("   ❌ 警告: 发现未脱敏的姓名!")
                    elif "[NAME]" in info['content']:
                        print("   ✅ 姓名已正确脱敏为 [NAME]")
                    else:
                        print("   ℹ️  此记录不包含姓名信息")
            else:
                print("ℹ️  未提取到新的医疗信息")
        else:
            print(f"❌ 患者识别失败: {result.get('error', '未知错误')}")
    
    # 检查数据库中存储的记录
    print(f"\n🗄️  检查数据库中的所有医疗记录:")
    print("-" * 40)
    
    patient_id = "P74B129D5"  # John Smith的ID
    records = rag.medical_db.get_patient_records(patient_id)
    
    privacy_violations = 0
    for record in records:
        print(f"类型: {record['type']}")
        print(f"内容: {record['content']}")
        
        if "John Smith" in record['content']:
            print("❌ 发现隐私泄露: 包含真实姓名!")
            privacy_violations += 1
        elif "[NAME]" in record['content']:
            print("✅ 隐私保护正确: 姓名已脱敏")
        else:
            print("ℹ️  此记录不涉及姓名")
        print()
    
    # 总结
    print("=" * 60)
    print("🎯 隐私保护测试总结:")
    if privacy_violations == 0:
        print("✅ 所有测试通过！隐私保护功能正常工作。")
        print("✅ 存储的医疗记录中不包含真实姓名。")
        print("✅ PII信息已正确替换为 [NAME] 标记。")
    else:
        print(f"❌ 发现 {privacy_violations} 处隐私泄露！")
        print("❌ 需要检查PII脱敏功能的实现。")
    
    return privacy_violations == 0

if __name__ == "__main__":
    success = test_privacy_protection()
    exit(0 if success else 1)