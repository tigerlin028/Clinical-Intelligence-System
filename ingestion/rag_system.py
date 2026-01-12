# RAG系统核心模块
import re
from typing import Dict, List, Optional, Tuple
from database import PatientDatabase, MedicalRecordsDatabase
import logging

logger = logging.getLogger(__name__)

class RAGSystem:
    """检索增强生成系统"""
    
    def __init__(self):
        self.patient_db = PatientDatabase()
        self.medical_db = MedicalRecordsDatabase()
    
    def extract_patient_info(self, transcript: str) -> Dict[str, str]:
        """从转录文本中提取患者信息"""
        patient_info = {}
        
        # 提取姓名 - 寻找 "my name is" 或 "I'm" 后面的内容
        name_patterns = [
            r"my name is ([A-Za-z\s]+)",
            r"I'm ([A-Za-z\s]+)",
            r"name is ([A-Za-z\s]+)",
            r"I am ([A-Za-z\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # 过滤掉常见的非姓名词汇
                if not any(word in name.lower() for word in ['suffering', 'having', 'feeling', 'experiencing']):
                    patient_info['name'] = name
                    break
        
        # 提取SSN - 寻找XXX-XX-XXXX格式
        ssn_pattern = r"\b(\d{3}[-\s]?\d{2}[-\s]?\d{4})\b"
        ssn_match = re.search(ssn_pattern, transcript)
        if ssn_match:
            ssn = re.sub(r'[-\s]', '-', ssn_match.group(1))
            if len(ssn.replace('-', '')) == 9:
                patient_info['ssn'] = ssn
        
        # 提取出生日期 - 寻找日期格式
        dob_patterns = [
            r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{4})\b",
            r"\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b",
            r"born on ([A-Za-z]+ \d{1,2},? \d{4})",
            r"birth.*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})"
        ]
        
        for pattern in dob_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                patient_info['dob'] = match.group(1).strip()
                break
        
        return patient_info
    
    def identify_patient(self, transcript: str) -> Optional[str]:
        """识别患者身份并返回patient_id"""
        patient_info = self.extract_patient_info(transcript)
        
        if not patient_info:
            logger.warning("No patient information found in transcript")
            return None
        
        logger.info(f"Extracted patient info: {patient_info}")
        
        # 尝试匹配患者
        patient_id = self.patient_db.find_patient(
            name=patient_info.get('name'),
            ssn=patient_info.get('ssn'),
            dob=patient_info.get('dob')
        )
        
        if patient_id:
            logger.info(f"Patient identified: {patient_id}")
        else:
            logger.warning("Patient not found in database")
        
        return patient_id
    
    def retrieve_medical_context(self, patient_id: str) -> List[Dict]:
        """检索患者的医疗记录作为上下文"""
        if not patient_id:
            return []
        
        records = self.medical_db.get_patient_records(patient_id)
        logger.info(f"Retrieved {len(records)} medical records for patient {patient_id}")
        
        return records
    
    def process_conversation(self, transcript: str) -> Dict:
        """处理完整的对话流程"""
        result = {
            'patient_identified': False,
            'patient_id': None,
            'medical_records': [],
            'extracted_info': {},
            'error': None
        }
        
        try:
            # 1. 提取患者信息
            patient_info = self.extract_patient_info(transcript)
            result['extracted_info'] = patient_info
            
            if not patient_info:
                result['error'] = "No patient information found in transcript"
                return result
            
            # 2. 识别患者
            patient_id = self.identify_patient(transcript)
            
            if not patient_id:
                result['error'] = "Patient not found in database"
                return result
            
            result['patient_identified'] = True
            result['patient_id'] = patient_id
            
            # 3. 检索医疗记录
            medical_records = self.retrieve_medical_context(patient_id)
            result['medical_records'] = medical_records
            
            # 4. 保存对话记录
            self.patient_db.add_conversation(patient_id, transcript)
            
            logger.info(f"Successfully processed conversation for patient {patient_id}")
            
        except Exception as e:
            logger.error(f"Error processing conversation: {str(e)}")
            result['error'] = str(e)
        
        return result
    
    def format_medical_records_for_display(self, records: List[Dict]) -> List[Dict]:
        """格式化医疗记录用于前端显示"""
        formatted_records = []
        
        for record in records:
            formatted_records.append({
                'type': record['type'],
                'content': record['content'],
                'date': record['date'],
                'category': self._categorize_record(record['type'])
            })
        
        return formatted_records
    
    def _categorize_record(self, record_type: str) -> str:
        """将记录类型分类"""
        categories = {
            'Medical History': 'history',
            'Previous Visit': 'visit',
            'Allergies': 'allergy',
            'Medications': 'medication',
            'Lab Results': 'lab',
            'Diagnosis': 'diagnosis'
        }
        
        return categories.get(record_type, 'other')


# 测试函数
def test_rag_system():
    """测试RAG系统"""
    from database import init_sample_data
    
    # 初始化示例数据
    init_sample_data()
    
    # 创建RAG系统
    rag = RAGSystem()
    
    # 测试转录文本
    test_transcript = """
    Hi, what can I help you? Hi, Dr. I'm John Smith. Currently I'm suffering from headache and I don't know why.
    Okay, what's the detail for that? And by the way, what's your day of birth in SSN?
    Oh, I born in 1985-03-15. And my SSN is 123-45-6789. Thank you.
    """
    
    # 处理对话
    result = rag.process_conversation(test_transcript)
    
    print("RAG System Test Results:")
    print(f"Patient Identified: {result['patient_identified']}")
    print(f"Patient ID: {result['patient_id']}")
    print(f"Extracted Info: {result['extracted_info']}")
    print(f"Medical Records Count: {len(result['medical_records'])}")
    
    if result['medical_records']:
        print("\nMedical Records:")
        for record in result['medical_records']:
            print(f"- {record['type']}: {record['content'][:100]}...")


if __name__ == "__main__":
    test_rag_system()