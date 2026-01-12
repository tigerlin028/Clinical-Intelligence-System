# Clinical Ambient Intelligence System

A microservices-based clinical ambient intelligence system for processing medical conversations with privacy-first design.

## Architecture

- **frontend/**     : Next.js UI (deployed on Vercel)
- **ingestion/**    : Audio ingestion & streaming (FastAPI on Google Cloud Run)
- **intelligence/** : PII redaction, RAG, reasoning (planned)

---

## Phase 1 Implementation Status

### ✅ Feature 1 — Cloud Infrastructure Setup

**Status:** Complete  
**Objective:** Validate core cloud architecture with end-to-end communication

- **Frontend:** Next.js UI deployed on Vercel with HTTPS
- **Backend:** FastAPI service on Google Cloud Run with proper CORS
- **Communication:** Verified end-to-end HTTPS communication
- **Error Handling:** Comprehensive error handling and user feedback

### ✅ Feature 3 — Audio Processing Pipeline

**Status:** Complete  
**Objective:** Convert audio to structured transcript with speaker identification

**Implementation:**
- **Audio Transcription:** Faster Whisper model (base, CPU optimized)
- **Speaker Diarization:** Enhanced heuristic-based speaker assignment
  - Patient indicators: "I feel", "I have", "my pain"
  - Medical questions: "what should I", "how do I"
  - Professional language detection
- **File Support:** All common audio formats (mp3, wav, m4a, etc.)

### ✅ Feature 4 — PII / PHI Redaction Layer

**Status:** Complete  
**Objective:** Privacy-first processing with automatic sensitive data redaction

**Implementation:**
- **Semantic Detection:** spaCy NER model for intelligent PII detection
- **Multi-layer Redaction:**
  - Always-on: Dates (multiple formats), SSN patterns
  - Conditional: Names (only when semantically detected)
- **Privacy Design:** Raw text never sent to frontend
- **Transparency:** Users see what was redacted and why

---

## Demo Usage

1. **Upload Audio:** Drag and drop or select audio file
2. **Processing:** System automatically:
   - Transcribes speech to text
   - Identifies speakers (Doctor/Patient)
   - Detects and redacts sensitive information
3. **Results:** View privacy-protected transcript with speaker labels

## Technical Features

- **Privacy-First:** All PII/PHI automatically redacted
- **Speaker Intelligence:** Context-aware speaker identification
- **Error Resilience:** Comprehensive error handling and recovery
- **Cloud-Native:** Scalable microservices architecture
- **Real-time Feedback:** Processing status and privacy notifications

---

## Next Phase Features (Planned)

- **Real-time Audio Streaming:** Live conversation processing
- **Advanced RAG:** Medical knowledge retrieval and reasoning
- **Clinical Insights:** Automated clinical note generation
- **Integration APIs:** EHR system connectivity

