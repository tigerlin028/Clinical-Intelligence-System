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
        
        # 3. PII 检测和脱敏
        logger.info("Starting PII detection and redaction...")
        full_text = " ".join([seg["text"] for seg in transcript])
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

        logger.info(f"Processing complete. Redacted entities: {list(all_redacted_entities)}")
        
        return {
            "transcript": redacted_transcript,
            "redaction_summary": list(all_redacted_entities),
            "detected_entity_types": detected_types,
            "processing_note": "Phase 1: Audio transcription with speaker identification and PII redaction",
            "segments_count": len(segments)
        }
        
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
    
@app.on_event("startup")
def startup_event():
    print("FastAPI started. Ready to accept requests.")

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
