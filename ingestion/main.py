from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uuid
from fastapi.middleware.cors import CORSMiddleware
from pii import redact_pii
from pii_ner import ner_detect_pii
from fastapi import UploadFile, File
import tempfile
import os
from asr.transcribe import transcribe_audio
from asr.diarize import assign_speakers
from fastapi import Response
import logging
from rag_system import RAGSystem

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Clinical Intelligence Ingestion Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://clinical-intelligence-system.vercel.app",
        "http://localhost:3000"  # 开发环境
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化RAG系统
rag_system = RAGSystem()

# ---------- 数据模型（统一 payload） ----------

class IngestRequest(BaseModel):
    text: str
    session_id: str | None = None
    speaker: str | None = None


class IngestResponse(BaseModel):
    session_id: str
    result: dict


# ---------- 核心处理逻辑（Feature 1 & 2 共用） ----------

def process_input(payload: dict) -> dict:
    raw_text = payload["content"]

    detected_types = ner_detect_pii(raw_text)

    redacted_text, entities = redact_pii(
        raw_text,
        allowed_types=detected_types
    )

    return {
        "raw_text": raw_text,
        "redacted_text": redacted_text,
        "redaction_summary": entities,
        "detected_by": "spacy_ner",
        "detected_entity_types": detected_types,
        "note": "phase1 semantic-assisted pii redaction"
    }

# ---------- HTTP Adapter（Feature 1 用） ----------

@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    session_id = req.session_id or str(uuid.uuid4())

    payload = {
        "session_id": session_id,
        "content": req.text,
        "speaker": req.speaker,
        "mode": "batch"
    }

    result = process_input(payload)

    return {
        "session_id": session_id,
        "result": result
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    logger.info(f"Received audio file: {file.filename}, size: {file.size}")
    
    # 验证文件类型
    if not file.content_type or not file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    # 保存临时文件
    suffix = os.path.splitext(file.filename or "audio.wav")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    logger.info(f"Saved temporary file: {tmp_path}")

    try:
        # 1. 转录音频
        logger.info("Starting audio transcription...")
        segments = transcribe_audio(tmp_path)
        logger.info(f"Transcription complete: {len(segments)} segments")
        
        # 2. 说话人识别
        logger.info("Assigning speakers...")
        transcript = assign_speakers(segments)
        
        # 3. 合并完整转录文本用于RAG处理
        full_text = " ".join([seg["text"] for seg in transcript])
        logger.info(f"Full transcript: {full_text[:200]}...")
        
        # 4. RAG系统处理 - 患者识别和医疗记录检索
        logger.info("Starting RAG processing...")
        rag_result = rag_system.process_conversation(full_text)
        
        # 5. PII 检测和脱敏
        logger.info("Starting PII detection and redaction...")
        detected_types = ner_detect_pii(full_text)
        logger.info(f"Detected PII types: {detected_types}")
        
        # 对每个片段进行脱敏
        redacted_transcript = []
        all_redacted_entities = set()
        
        for seg in transcript:
            redacted_text, entities = redact_pii(
                seg["text"],
                allowed_types=detected_types
            )
            redacted_transcript.append({
                "speaker": seg["speaker"],
                "text": redacted_text
            })
            all_redacted_entities.update(entities)

        logger.info(f"Processing complete. Patient identified: {rag_result['patient_identified']}")
        
        # 6. 构建响应
        response = {
            "transcript": redacted_transcript,
            "redaction_summary": list(all_redacted_entities),
            "detected_entity_types": detected_types,
            "processing_note": "Phase 1: Audio transcription with speaker identification, PII redaction, and medical record retrieval",
            "segments_count": len(segments),
            # RAG结果
            "patient_identified": rag_result["patient_identified"],
            "patient_id": rag_result["patient_id"],
            "medical_records": rag_result["medical_records"],
            "extracted_patient_info": rag_result["extracted_info"]
        }
        
        # 如果有RAG错误，添加到响应中
        if rag_result.get("error"):
            response["rag_error"] = rag_result["error"]
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")
    finally:
        # 清理临时文件
        try:
            os.remove(tmp_path)
            logger.info(f"Cleaned up temporary file: {tmp_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary file: {e}")


@app.get("/patient/{patient_id}/records")
async def get_patient_records(patient_id: str):
    """获取特定患者的医疗记录"""
    try:
        records = rag_system.retrieve_medical_context(patient_id)
        return {
            "patient_id": patient_id,
            "records": records,
            "count": len(records)
        }
    except Exception as e:
        logger.error(f"Error retrieving patient records: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/medical-record/{record_id}")
async def delete_medical_record(record_id: int):
    """删除特定的医疗记录"""
    try:
        success = rag_system.delete_medical_record(record_id)
        if success:
            return {"message": "Medical record deleted successfully", "record_id": record_id}
        else:
            raise HTTPException(status_code=404, detail="Medical record not found")
    except Exception as e:
        logger.error(f"Error deleting medical record: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/initialize-sample-data")
async def initialize_sample_data():
    """初始化示例数据（仅用于演示）"""
    try:
        from database import init_sample_data
        init_sample_data()
        return {"message": "Sample data initialized successfully"}
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.on_event("startup")
def startup_event():
    print("FastAPI started. Ready to accept requests.")
    # 注释掉自动初始化，避免重复数据
    # try:
    #     from database import init_sample_data
    #     init_sample_data()
    #     logger.info("Sample data initialized on startup")
    # except Exception as e:
    #     logger.warning(f"Failed to initialize sample data: {e}")

@app.options("/upload-audio")
def options_upload_audio():
    return Response(
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": "https://clinical-intelligence-system.vercel.app",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )