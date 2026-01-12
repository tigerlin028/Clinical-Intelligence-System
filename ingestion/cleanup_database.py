#!/usr/bin/env python3
"""
清理数据库中的重复记录
"""

import sqlite3
import os

def cleanup_duplicate_records():
    """清理medical_records表中的重复记录"""
    db_path = "medical_records.db"
    
    if not os.path.exists(db_path):
        print("Database file not found. Nothing to clean up.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查看当前记录数
    cursor.execute("SELECT COUNT(*) FROM medical_records")
    total_before = cursor.fetchone()[0]
    print(f"Total records before cleanup: {total_before}")
    
    # 删除重复记录，保留最早的一条
    cursor.execute('''
        DELETE FROM medical_records 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM medical_records 
            GROUP BY patient_id, record_type, content
        )
    ''')
    
    deleted_count = cursor.rowcount
    conn.commit()
    
    # 查看清理后的记录数
    cursor.execute("SELECT COUNT(*) FROM medical_records")
    total_after = cursor.fetchone()[0]
    
    print(f"Deleted {deleted_count} duplicate records")
    print(f"Total records after cleanup: {total_after}")
    
    # 显示剩余记录
    cursor.execute('''
        SELECT patient_id, record_type, content, date_recorded 
        FROM medical_records 
        ORDER BY patient_id, date_recorded
    ''')
    
    print("\nRemaining records:")
    for row in cursor.fetchall():
        print(f"  {row[0]} | {row[1]} | {row[2][:50]}... | {row[3]}")
    
    conn.close()

def reset_database():
    """完全重置数据库"""
    db_files = ["medical_records.db", "patients.db"]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"Removed {db_file}")
    
    print("Database reset complete. Run the server to reinitialize with sample data.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        cleanup_duplicate_records()