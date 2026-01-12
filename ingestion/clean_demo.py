#!/usr/bin/env python3
"""
重构后的数据库清理脚本
- patients.db: 只存储患者身份信息
- medical_records.db: 存储医疗记录和对话记录
"""

import sqlite3
import os
from database import PatientDatabase, MedicalRecordsDatabase

def inspect_current_state():
    """检查当前数据库状态"""
    print("🔍 检查当前数据库状态...")
    
    # 检查patients.db
    if os.path.exists("patients.db"):
        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()
        
        # 检查所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📊 patients.db 包含的表: {[t[0] for t in tables]}")
        
        # 检查patients表
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        print(f"   - patients表: {patient_count} 个患者")
        
        # 检查是否还有conversations表（应该被移除）
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM conversations")
            conv_count = cursor.fetchone()[0]
            print(f"   - conversations表: {conv_count} 条记录 (应该被移除)")
        
        conn.close()
    
    # 检查medical_records.db
    if os.path.exists("medical_records.db"):
        conn = sqlite3.connect("medical_records.db")
        cursor = conn.cursor()
        
        # 检查所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📊 medical_records.db 包含的表: {[t[0] for t in tables]}")
        
        # 检查medical_records表
        cursor.execute("SELECT COUNT(*) FROM medical_records")
        record_count = cursor.fetchone()[0]
        print(f"   - medical_records表: {record_count} 条记录")
        
        # 检查conversations表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM conversations")
            conv_count = cursor.fetchone()[0]
            print(f"   - conversations表: {conv_count} 条记录")
        
        conn.close()

def clean_and_restructure():
    """清理并重构数据库"""
    print("\n🧹 清理并重构数据库...")
    
    # 1. 完全删除旧的数据库文件
    for db_file in ["patients.db", "medical_records.db"]:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ 已删除 {db_file}")
    
    # 2. 重新初始化数据库（使用新结构）
    print("🔄 重新初始化数据库...")
    patient_db = PatientDatabase()
    medical_db = MedicalRecordsDatabase()
    
    # 3. 只添加John Smith的基础信息
    print("👤 添加John Smith的基础信息...")
    patient_id = patient_db.add_patient("John Smith", "123-45-6789", "1985-03-15")
    print(f"✅ 创建患者: {patient_id}")
    
    # 4. 只添加最基础的医疗记录
    print("📋 添加基础医疗记录...")
    
    medical_db.add_record(patient_id, "Medical History", 
                         "Patient has a history of hypertension and diabetes. Currently on Metformin 500mg twice daily.")
    
    medical_db.add_record(patient_id, "Previous Visit", 
                         "Last visit on 2024-01-10: Blood pressure 140/90, HbA1c 7.2%. Recommended diet modification.")
    
    medical_db.add_record(patient_id, "Allergies", 
                         "Allergic to Penicillin - causes rash and swelling.")
    
    print("✅ 基础医疗记录添加完成")

def verify_new_structure():
    """验证新的数据库结构"""
    print("\n🔍 验证新的数据库结构...")
    
    # 验证patients.db结构
    print("📊 patients.db 结构:")
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"   表: {tables}")
    
    cursor.execute("SELECT COUNT(*) FROM patients")
    patient_count = cursor.fetchone()[0]
    print(f"   患者数量: {patient_count}")
    
    # 确认没有conversations表
    if 'conversations' in tables:
        print("   ❌ 警告: patients.db中仍有conversations表")
    else:
        print("   ✅ 正确: patients.db中没有conversations表")
    
    conn.close()
    
    # 验证medical_records.db结构
    print("\n📊 medical_records.db 结构:")
    conn = sqlite3.connect("medical_records.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"   表: {tables}")
    
    cursor.execute("SELECT COUNT(*) FROM medical_records")
    record_count = cursor.fetchone()[0]
    print(f"   医疗记录数量: {record_count}")
    
    cursor.execute("SELECT COUNT(*) FROM conversations")
    conv_count = cursor.fetchone()[0]
    print(f"   对话记录数量: {conv_count}")
    
    conn.close()

def main():
    """主函数"""
    print("🚀 重构数据库结构")
    print("=" * 60)
    print("目标:")
    print("- patients.db: 只存储患者身份信息")
    print("- medical_records.db: 存储医疗记录和对话记录")
    print("=" * 60)
    
    # 检查当前状态
    inspect_current_state()
    
    # 清理并重构
    clean_and_restructure()
    
    # 验证新结构
    verify_new_structure()
    
    print("\n" + "=" * 60)
    print("✨ 数据库重构完成！")
    print("\n📋 新的数据库结构:")
    print("✅ patients.db - 只有患者身份信息")
    print("✅ medical_records.db - 医疗记录 + 对话记录")
    print("\n🎯 现在可以开始全新的demo了！")

if __name__ == "__main__":
    main()