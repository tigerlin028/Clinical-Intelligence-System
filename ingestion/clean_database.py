#!/usr/bin/env python3
"""
数据库清理脚本 - 清除现有的未脱敏医疗记录
"""

import sqlite3
import os
from database import PatientDatabase, MedicalRecordsDatabase

def clean_medical_records():
    """清除所有医疗记录，保留患者身份信息"""
    print("🧹 开始清理医疗记录数据库...")
    
    # 删除医疗记录数据库文件
    if os.path.exists("medical_records.db"):
        os.remove("medical_records.db")
        print("✅ 已删除旧的医疗记录数据库")
    
    # 重新初始化医疗记录数据库
    medical_db = MedicalRecordsDatabase()
    print("✅ 已重新初始化医疗记录数据库")
    
    # 重新添加示例数据（这些是预设的，不包含PII）
    patient_id1 = "P74B129D5"  # John Smith的ID
    
    medical_db.add_record(patient_id1, "Medical History", 
                         "Patient has a history of hypertension and diabetes. Currently on Metformin 500mg twice daily.")
    
    medical_db.add_record(patient_id1, "Previous Visit", 
                         "Last visit on 2024-01-10: Blood pressure 140/90, HbA1c 7.2%. Recommended diet modification.")
    
    medical_db.add_record(patient_id1, "Allergies", 
                         "Allergic to Penicillin - causes rash and swelling.")
    
    print("✅ 已重新添加基础医疗记录（不含PII）")
    print("🎉 数据库清理完成！现在所有新的音频转录都会自动进行PII脱敏。")

def clean_conversations():
    """清除对话记录"""
    print("🧹 开始清理对话记录...")
    
    try:
        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        if cursor.fetchone():
            # 清除所有对话记录
            cursor.execute("DELETE FROM conversations")
            conn.commit()
            count = cursor.rowcount
            print(f"✅ 已清除 {count} 条对话记录")
        else:
            print("ℹ️  对话记录表不存在，跳过清理")
        
        conn.close()
    except Exception as e:
        print(f"⚠️  清理对话记录时出错: {e}")
        print("ℹ️  这通常不影响系统正常运行")

def main():
    """主函数"""
    print("🚀 开始数据库清理...")
    print("=" * 50)
    
    clean_medical_records()
    clean_conversations()
    
    print("=" * 50)
    print("✨ 数据库清理完成！")
    print("\n📋 接下来的步骤：")
    print("1. 重新启动后端服务")
    print("2. 上传新的音频文件测试")
    print("3. 验证存储的医疗记录中名字已被替换为 [NAME]")

if __name__ == "__main__":
    main()