# Clinical Ambient Intelligence System

A microservices-based clinical ambient intelligence system.

## Architecture

- frontend/     : Next.js UI
- ingestion/    : Audio ingestion & streaming
- intelligence/ : PII redaction, RAG, reasoning

## Phase 1 · Feature 1 — Cloud Infrastructure Setup

**Objective**  
Validate the core cloud architecture of the Clinical Ambient Intelligence System by deploying all services to the public internet and verifying end-to-end communication. This feature focuses on infrastructure correctness rather than AI capability.

**Architecture**  
Browser (Next.js, Vercel) → Ingestion Service (FastAPI, Cloud Run) → Intelligence Logic (Phase 1 stub)

**Implementation**  
- **Frontend:** Deployed on Vercel; sends a test string via HTTPS.  
- **Ingestion Service:** Dockerized FastAPI service deployed on Google Cloud Run; acts as an adapter layer to normalize input and route requests.  
- **Intelligence Logic:** Mock implementation to validate data flow before introducing PII redaction or RAG.

**End-to-End Flow**  
User triggers request in the browser → frontend sends JSON to Ingestion Service → intelligence logic processes input → structured response is returned and logged in the browser console.

**Status**  
Feature 1 complete. Public HTTPS communication, CORS handling, and cloud deployment are verified. Real-time streaming and AI logic are deferred to later features.
