# Clinical Ambient Intelligence System

A microservices-based clinical ambient intelligence system.

## Architecture

- frontend/     : Next.js UI
- ingestion/    : Audio ingestion & streaming
- intelligence/ : PII redaction, RAG, reasoning

---

## Phase 1 · Feature 1 — Cloud Infrastructure Setup

**Objective**  
Validate the core cloud architecture by deploying all services to the public internet and verifying end-to-end communication. This feature focuses on infrastructure correctness rather than AI capability.

**Architecture**  
Browser (Next.js, Vercel) → Ingestion Service (FastAPI, Cloud Run) → Intelligence Logic (Phase 1 stub)

**Implementation**  
- **Frontend:** Next.js UI deployed on Vercel; sends test input via HTTPS.  
- **Ingestion Service:** Dockerized FastAPI service deployed on Google Cloud Run; normalizes requests and manages sessions.  
- **Intelligence Logic:** Stubbed processing layer to validate data flow before introducing AI features.

**End-to-End Flow**  
User action in browser → JSON request to Ingestion Service → intelligence logic processes input → response returned and logged in browser console.

**Status**  
Feature 1 complete. Public HTTPS access, CORS handling, and cloud deployment are verified. Real-time streaming and AI logic are deferred to later features.

---

## Phase 1 · Feature 4 — PII / PHI Redaction Layer

**Objective**  
Establish a privacy boundary by detecting and redacting sensitive clinical information (PII / PHI) before any text is displayed in the UI or used for downstream processing.

**Architecture Extension**  
Browser → Ingestion Service → Semantic PII Detector → Deterministic Redactor → Redacted Output

**Implementation**  
- **Semantic Detection:** Local spaCy NER model identifies whether name redaction should be attempted.  
- **Deterministic Redaction:** Rule-based masking for high-certainty entities (e.g., SSN, dates), with name redaction gated by semantic detection.  
- **Safety Design:** Raw text is retained server-side for processing but never rendered in the UI.

**Data Flow**  
Input text → PII detection → redaction → redacted text returned to frontend and downstream logic.

**Status**  
Feature 4 complete. Server-side PII redaction is enforced, UI displays only redacted content, and the system is prepared for retrieval and reasoning features.

