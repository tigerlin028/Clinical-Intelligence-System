from fastapi import FastAPI
from pydantic import BaseModel
import requests
import uuid
from fastapi.middleware.cors import CORSMiddleware

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
    """
    这是未来 100% 复用的核心逻辑
    HTTP / WebSocket 只负责把数据送进来
    """

    # 🚧 Phase 1：mock Intelligence Service
    # 后面我们会替换成真实 Lambda
    intelligence_response = {
        "processed_text": payload["content"].upper(),
        "note": "mock intelligence result"
    }

    return intelligence_response


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
