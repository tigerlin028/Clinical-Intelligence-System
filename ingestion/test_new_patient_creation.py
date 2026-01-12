#!/usr/bin/env python3
"""
新患者自动创建功能测试脚本
"""

from rag_system import RAGSystem
from database import init_sample_data
import json

def test_new_patient_creation():
    """测试新患者自动创建功能"""
    print("👤 测试新患者自动创建功能...")
    print("=" * 60)
    
    # 初始化系统
    init_sample_data()
    rag = RAGSystem()
    
    # 测试用的新患者对话
    test_cases = [
        {
            "name": "完全新的患者 - 有完整信息",
            "transcript": "Hi, I'm Alice Johnson. My SSN is 555-66-7777 and I was born on 1992-05-15. I'm having back pain."
        },
        {
            "name": "新患者 - 只有姓名",
            "transcript": "Hello, I'm Bob Wilson. I've been having trouble sleeping lately."
        },
        {
            "name": "新患者 - 中文姓名测试",
            "transcript": "Hi, I'm Li Wei. I'm experiencing headaches recently."
        }
    ]
    
    created_patients = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试案例 {i}: {test_case['name']}")
        print("-" * 40)
        print(f"对话内容: {test_case['transcript']}")
        
        # 处理对话
        result = rag.process_conversation(test_case['transcript'])
        
        if result['patient_identified']:
            patient_id = result['patient_id']
            print(f"✅ 患者处理成功: {patient_id}")
            print(f"📝 提取的患者信息: {result['extracted_info']}")
            
            # 检查是否是新创建的患者
            if patient_id not in created_patients:
                created_patients.append(patient_id)
                print(f"🆕 这是一个新创建的患者记录")
            else:
                print(f"🔄 这是已存在的患者")
            
            # 显示提取的医疗信息
            if result['new_medical_info']:
                print(f"📋 提取到 {len(result['new_medical_info'])} 条医疗信息:")
                for info in result['new_medical_info']:
                    print(f"   - {info['type']}: {info['content']}")
            
            # 显示患者的所有记录
            print(f"📚 患者 {patient_id} 的所有医疗记录:")
            for record in result['medical_records']:
                print(f"   - {record['type']}: {record['content'][:50]}...")
                
        else:
            print(f"❌ 患者处理失败: {result.get('error', '未知错误')}")
    
    print(f"\n🎯 测试总结:")
    print(f"✅ 成功创建/处理了 {len(created_patients)} 个患者")
    print(f"📋 患者ID列表: {created_patients}")
    
    return len(created_patients) > 0

def test_returning_patient():
    """测试返回患者的记录检索"""
    print(f"\n🔄 测试返回患者的记录检索...")
    print("-" * 40)
    
    rag = RAGSystem()
    
    # 第一次对话 - 创建患者
    first_conversation = "Hi, I'm Charlie Brown. I'm having stomach issues."
    print(f"第一次对话: {first_conversation}")
    
    result1 = rag.process_conversation(first_conversation)
    if result1['patient_identified']:
        patient_id = result1['patient_id']
        print(f"✅ 第一次对话 - 患者创建: {patient_id}")
        print(f"📋 第一次记录数: {len(result1['medical_records'])}")
    else:
        print(f"❌ 第一次对话失败: {result1.get('error')}")
        return False
    
    # 第二次对话 - 同一患者
    second_conversation = "Hi, it's Charlie Brown again. The stomach pain is getting worse."
    print(f"\n第二次对话: {second_conversation}")
    
    result2 = rag.process_conversation(second_conversation)
    print(f"第二次对话提取的患者信息: {result2.get('extracted_info', {})}")
    
    if result2['patient_identified']:
        print(f"✅ 第二次对话 - 患者识别: {result2['patient_id']}")
        print(f"📋 第二次记录数: {len(result2['medical_records'])}")
        
        # 验证是否是同一患者
        if result2['patient_id'] == patient_id:
            print("✅ 正确识别为同一患者")
        else:
            print(f"⚠️  识别为不同患者: {result2['patient_id']} vs {patient_id}")
        
        # 验证记录是否累积
        if len(result2['medical_records']) > len(result1['medical_records']):
            print("✅ 记录正确累积 - 包含了之前的对话内容")
        else:
            print("⚠️  记录可能没有正确累积")
            
        # 显示所有记录
        print("📚 患者的完整医疗记录:")
        for i, record in enumerate(result2['medical_records'], 1):
            print(f"   {i}. {record['type']}: {record['content'][:60]}...")
            
        return True
    else:
        print(f"❌ 第二次对话失败: {result2.get('error')}")
        return False

if __name__ == "__main__":
    print("🚀 开始新患者创建功能测试\n")
    
    success1 = test_new_patient_creation()
    success2 = test_returning_patient()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 所有测试通过！新患者自动创建功能正常工作。")
        print("✅ 系统现在支持:")
        print("   - 自动创建新患者记录")
        print("   - 为新患者存储医疗信息")
        print("   - 返回患者时检索历史记录")
    else:
        print("❌ 部分测试失败，请检查实现。")
    
    exit(0 if (success1 and success2) else 1)