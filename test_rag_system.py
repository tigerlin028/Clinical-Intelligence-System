#!/usr/bin/env python3
"""
RAG系统完整测试脚本
测试从文本输入到医疗记录检索的完整流程
"""

import requests
import json

# API配置
API_BASE = "https://ingestion-service-523658399118.us-central1.run.app"

def test_health():
    """测试服务健康状态"""
    print("🔍 Testing service health...")
    response = requests.get(f"{API_BASE}/health")
    print(f"Health check: {response.json()}")
    return response.status_code == 200

def test_initialize_data():
    """初始化示例数据"""
    print("📊 Initializing sample data...")
    response = requests.post(f"{API_BASE}/initialize-sample-data")
    print(f"Data initialization: {response.json()}")
    return response.status_code == 200

def test_patient_records():
    """测试患者记录检索"""
    print("🏥 Testing patient records retrieval...")
    # John Smith的患者ID
    patient_id = "P74B129D5"
    response = requests.get(f"{API_BASE}/patient/{patient_id}/records")
    data = response.json()
    print(f"Patient {patient_id} has {data['count']} records")
    
    if data['records']:
        print("Sample records:")
        for i, record in enumerate(data['records'][:2]):  # 显示前2条
            print(f"  {i+1}. {record['type']}: {record['content'][:50]}...")
    
    return response.status_code == 200 and data['count'] > 0

def test_text_processing():
    """测试文本处理和RAG功能"""
    print("🤖 Testing text processing with RAG...")
    
    test_text = """
    Hi Doctor, my name is John Smith. I'm currently suffering from headaches 
    and I don't know why. My date of birth is 1985-03-15 and my SSN is 123-45-6789.
    """
    
    payload = {
        "text": test_text.strip(),
        "session_id": "test-rag-session"
    }
    
    response = requests.post(
        f"{API_BASE}/ingest",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        result = data['result']
        
        print("✅ Text processing successful!")
        print(f"Original text: {result['raw_text'][:50]}...")
        print(f"Redacted text: {result['redacted_text'][:50]}...")
        print(f"Detected PII types: {result['detected_entity_types']}")
        print(f"Redacted entities: {result['redaction_summary']}")
        
        return True
    else:
        print(f"❌ Text processing failed: {response.status_code}")
        print(response.text)
        return False

def main():
    """运行所有测试"""
    print("🚀 Starting RAG System Tests\n")
    
    tests = [
        ("Service Health", test_health),
        ("Data Initialization", test_initialize_data),
        ("Patient Records", test_patient_records),
        ("Text Processing", test_text_processing),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            success = test_func()
            results.append((test_name, success))
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"\n{test_name}: {status}")
        except Exception as e:
            print(f"\n{test_name}: ❌ ERROR - {str(e)}")
            results.append((test_name, False))
    
    # 总结
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! RAG system is working correctly.")
        print("\n📋 Next steps:")
        print("1. Visit https://clinical-intelligence-system.vercel.app/")
        print("2. Upload an audio file with patient information")
        print("3. Verify that medical records are displayed")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()