#!/usr/bin/env python3
"""
简单的患者流程测试
"""

from rag_system import RAGSystem
from database import init_sample_data

def test_simple_flow():
    """测试简单的患者创建和识别流程"""
    print("🧪 简单患者流程测试")
    print("=" * 50)
    
    # 初始化
    init_sample_data()
    rag = RAGSystem()
    
    # 测试1: 新患者 - 第一次对话
    print("\n📋 测试1: 新患者第一次对话")
    conversation1 = "Hi, I'm David Smith. I have a headache."
    result1 = rag.process_conversation(conversation1)
    
    if result1['patient_identified']:
        patient_id = result1['patient_id']
        print(f"✅ 患者创建成功: {patient_id}")
        print(f"📝 提取信息: {result1['extracted_info']}")
        print(f"📋 医疗记录数: {len(result1['medical_records'])}")
    else:
        print(f"❌ 失败: {result1.get('error')}")
        return False
    
    # 测试2: 同一患者 - 第二次对话（使用相同的表达方式）
    print(f"\n📋 测试2: 同一患者第二次对话")
    conversation2 = "Hi, I'm David Smith. The headache is worse now."
    result2 = rag.process_conversation(conversation2)
    
    if result2['patient_identified']:
        print(f"✅ 患者识别成功: {result2['patient_id']}")
        print(f"📝 提取信息: {result2['extracted_info']}")
        print(f"📋 医疗记录数: {len(result2['medical_records'])}")
        
        # 检查是否是同一患者
        if result2['patient_id'] == patient_id:
            print("✅ 正确识别为同一患者")
            if len(result2['medical_records']) > len(result1['medical_records']):
                print("✅ 记录正确累积")
                return True
            else:
                print("⚠️  记录未正确累积")
                return False
        else:
            print(f"❌ 识别为不同患者: {result2['patient_id']} vs {patient_id}")
            return False
    else:
        print(f"❌ 失败: {result2.get('error')}")
        return False

if __name__ == "__main__":
    success = test_simple_flow()
    if success:
        print("\n🎉 测试通过！新患者创建和识别功能正常工作。")
    else:
        print("\n❌ 测试失败。")
    exit(0 if success else 1)