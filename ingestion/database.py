# 数据库管理模块
import sqlite3
import json
from typing import Dict, List, Optional, Tuple
import hashlib
from datetime import datetime

class PatientDatabase:
    """患者身份信息数据库"""
    
    def __init__(self, db_path: str = "patients.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 患者身份信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name_hash TEXT NOT NULL,
                ssn_hash TEXT NOT NULL,
                dob_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 对话记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                transcript TEXT NOT NULL,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_pii(self, value: str) -> str:
        """对PII信息进行哈希处理"""
        return hashlib.sha256(value.lower().strip().encode()).hexdigest()
    
    def add_patient(self, name: str, ssn: str, dob: str) -> str:
        """添加新患者"""
        patient_id = f"P{hashlib.md5(f'{name}{ssn}{dob}'.encode()).hexdigest()[:8].upper()}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO patients (patient_id, name_hash, ssn_hash, dob_hash)
            VALUES (?, ?, ?, ?)
        ''', (patient_id, self.hash_pii(name), self.hash_pii(ssn), self.hash_pii(dob)))
        
        conn.commit()
        conn.close()
        
        return patient_id
    
    def find_patient(self, name: str = None, ssn: str = None, dob: str = None) -> Optional[str]:
        """根据PII信息查找患者ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        conditions = []
        params = []
        
        if name:
            conditions.append("name_hash = ?")
            params.append(self.hash_pii(name))
        
        if ssn:
            conditions.append("ssn_hash = ?")
            params.append(self.hash_pii(ssn))
        
        if dob:
            conditions.append("dob_hash = ?")
            params.append(self.hash_pii(dob))
        
        if not conditions:
            conn.close()
            return None
        
        query = f"SELECT patient_id FROM patients WHERE {' AND '.join(conditions)}"
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
    
    def add_conversation(self, patient_id: str, transcript: str, summary: str = None):
        """添加对话记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (patient_id, transcript, summary)
            VALUES (?, ?, ?)
        ''', (patient_id, transcript, summary))
        
        conn.commit()
        conn.close()


class MedicalRecordsDatabase:
    """医疗记录向量数据库（简化版）"""
    
    def __init__(self, db_path: str = "medical_records.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化医疗记录数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                record_type TEXT NOT NULL,
                content TEXT NOT NULL,
                date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_record(self, patient_id: str, record_type: str, content: str, metadata: Dict = None):
        """添加医疗记录（避免重复）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已存在相同的记录
        cursor.execute('''
            SELECT id FROM medical_records 
            WHERE patient_id = ? AND record_type = ? AND content = ?
        ''', (patient_id, record_type, content))
        
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO medical_records (patient_id, record_type, content, metadata)
                VALUES (?, ?, ?, ?)
            ''', (patient_id, record_type, content, json.dumps(metadata) if metadata else None))
            conn.commit()
            print(f"Added new medical record: {record_type} for {patient_id}")
        else:
            print(f"Record already exists, skipping: {record_type} for {patient_id}")
        
        conn.close()
    
    def get_patient_records(self, patient_id: str) -> List[Dict]:
        """获取患者的所有医疗记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT record_type, content, date_recorded, metadata
            FROM medical_records
            WHERE patient_id = ?
            ORDER BY date_recorded DESC
        ''', (patient_id,))
        
        records = []
        for row in cursor.fetchall():
            records.append({
                'type': row[0],
                'content': row[1],
                'date': row[2],
                'metadata': json.loads(row[3]) if row[3] else {}
            })
        
        conn.close()
        return records


# 初始化示例数据
def init_sample_data():
    """初始化一些示例数据用于演示"""
    
    # 患者数据库
    patient_db = PatientDatabase()
    
    # 添加示例患者
    patient_id1 = patient_db.add_patient("John Smith", "123-45-6789", "1985-03-15")
    patient_id2 = patient_db.add_patient("Mary Johnson", "987-65-4321", "1990-07-22")
    
    # 医疗记录数据库
    medical_db = MedicalRecordsDatabase()
    
    # 添加示例医疗记录
    medical_db.add_record(patient_id1, "Medical History", 
                         "Patient has a history of hypertension and diabetes. Currently on Metformin 500mg twice daily.")
    
    medical_db.add_record(patient_id1, "Previous Visit", 
                         "Last visit on 2024-01-10: Blood pressure 140/90, HbA1c 7.2%. Recommended diet modification.")
    
    medical_db.add_record(patient_id1, "Allergies", 
                         "Allergic to Penicillin - causes rash and swelling.")
    
    medical_db.add_record(patient_id2, "Medical History", 
                         "Patient has asthma since childhood. Uses Albuterol inhaler as needed.")
    
    medical_db.add_record(patient_id2, "Previous Visit", 
                         "Last visit on 2024-01-05: Respiratory function normal, no acute symptoms.")
    
    print(f"Sample data initialized:")
    print(f"Patient 1 ID: {patient_id1}")
    print(f"Patient 2 ID: {patient_id2}")


if __name__ == "__main__":
    init_sample_data()