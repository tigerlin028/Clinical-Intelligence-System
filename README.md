# Clinical Ambient Intelligence System

A microservices-based clinical ambient intelligence system.

## Architecture

- frontend/     : Next.js UI
- ingestion/    : Audio ingestion & streaming
- intelligence/ : PII redaction, RAG, reasoning

# Phase 1 · Feature 1  
## Cloud Infrastructure Setup

### Goal
Validate the core cloud architecture of the Clinical Ambient Intelligence System by deploying all services to the public internet and verifying end-to-end communication. This feature focuses strictly on infrastructure correctness, not AI intelligence.

---

### Architecture
Browser (Next.js, Vercel)
↓ HTTPS
Ingestion Service (FastAPI, Cloud Run)
↓
Intelligence Logic (Phase 1 Stub)


---

### Implementation
- **Frontend**: Next.js app deployed on Vercel, provides a minimal UI and sends test input.
- **Ingestion Service**: Dockerized FastAPI service deployed on Google Cloud Run. Acts as an adapter layer that normalizes input and routes data to the intelligence logic.
- **Intelligence Logic**: Mock implementation used to validate system wiring before introducing PII handling or RAG.

---

### End-to-End Flow
1. User triggers a request from the deployed frontend.
2. Frontend sends a JSON payload to the Ingestion Service.
3. Ingestion processes the request and invokes the intelligence stub.
4. Structured response is returned and logged in the browser console.

---

### Status
- All services are publicly accessible over HTTPS.
- CORS configured for secure browser access.
- End-to-end data flow verified.
- Feature 1 complete; real-time streaming and AI logic deferred to later features.
