from fastapi import FastAPI
from pydantic import BaseModel
import requests
import uuid
from fastapi.middleware.cors import CORSMiddleware
from pii import redact_pii
from pii_ner import ner_detect_pii

app = FastAPI(title="Ingestion Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://clinical-intelligence-system.vercel.app"
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
