# Clinical Ambient Intelligence System

A microservices-based clinical ambient intelligence system for processing medical conversations with privacy-first design and intelligent patient record management.

## Architecture

- **frontend/**     : Next.js UI (deployed on Vercel)
- **ingestion/**    : Audio ingestion, RAG system & medical records (FastAPI on Google Cloud Run)

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
- **Enhanced Speaker Diarization:** Rule-based speaker assignment with medical context
  - **Doctor Detection:** "What can I help you?", "Let me examine", professional greetings
  - **Patient Detection:** "I am [name]", "I feel", "I have", symptom descriptions
  - **Context-Aware:** Intelligent switching based on medical conversation patterns
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

### ✅ Feature 5 — RAG System & Medical Records

**Status:** Complete  
**Objective:** Intelligent patient identification and medical record retrieval

**Implementation:**
- **Patient Identification:** 
  - Smart name extraction from conversations ("I am Jack Stuart" → "Jack Stuart")
  - Automatic patient matching and creation
  - Privacy-protected storage with hash-based matching
- **Medical Records Database:**
  - Automatic conversation logging with PII redaction
  - Medical information extraction (symptoms, medications, notes)
  - Historical record retrieval for context
- **RAG Processing:**
  - Extract patient info from original text for matching
  - Store redacted versions for privacy
  - Link conversations to patient records

---

## Demo Usage

1. **Upload Audio:** Drag and drop or select audio file
2. **Processing:** System automatically:
   - Transcribes speech to text
   - Identifies speakers (Doctor/Patient) using medical context
   - Detects and redacts sensitive information
   - Identifies or creates patient records
   - Extracts and stores medical information
3. **Results:** View privacy-protected transcript with:
   - Speaker identification
   - Patient identification status
   - Medical records context
   - Privacy protection summary

## Technical Features

- **Privacy-First:** All PII/PHI automatically redacted before storage/display
- **Intelligent Patient Matching:** Extract names from original text, store redacted versions
- **Medical Context-Aware:** Speaker identification optimized for clinical conversations
- **Automatic Record Keeping:** Medical information extraction and storage
- **Error Resilience:** Comprehensive error handling and recovery
- **Cloud-Native:** Scalable microservices architecture
- **Real-time Feedback:** Processing status and privacy notifications

## Database Structure

- **patients.db:** Patient identity information (hashed for privacy)
- **medical_records.db:** Medical records, conversations, and extracted information

---

## Next Phase Features (Planned)

- **Real-time Audio Streaming:** Live conversation processing
- **Advanced RAG:** Medical knowledge retrieval and reasoning
- **Clinical Insights:** Automated clinical note generation
- **Integration APIs:** EHR system connectivity
- **Advanced Speaker Models:** ML-based speaker identification

