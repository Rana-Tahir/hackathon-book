# Implementation Plan: Physical AI & Humanoid Robotics — AI-Native Textbook

**Branch**: `001-physical-ai-book` | **Date**: 2026-02-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-book/spec.md`
**Constitution**: v2.0.0

## Summary

Build and deploy the AI-native platform layer for an existing 4-module
Physical AI textbook. The book content (36 markdown chapters) and code
artifacts (ROS 2, Gazebo, Nav2, VLA) are already written. The remaining
work is: (1) configure the Docusaurus site properly, (2) build the
FastAPI + Qdrant + Neon RAG chatbot backend, (3) embed the chatbot into
the frontend, (4) implement the embedding pipeline, and (5) deploy
publicly via Vercel.

## Technical Context

**Language/Version**: Python 3.10 (backend), TypeScript/React (frontend)
**Primary Dependencies**: FastAPI, Qdrant Client, Neon (asyncpg),
  OpenAI SDK, Docusaurus 3.x, React 19
**Storage**: Qdrant Cloud (vector store), Neon Serverless Postgres
  (structured data, chat history)
**Testing**: pytest (backend), Docusaurus build validation (frontend)
**Target Platform**: Vercel (frontend), Railway or Render (backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: RAG response < 3s, site load < 2s on 3G
**Constraints**: Qdrant Free Tier limits, CPU-only for book + RAG,
  no 24GB+ VRAM, embedding chunks 500–800 tokens
**Scale/Scope**: ~36 chapters, ~200 embeddings estimated, single
  deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Gate | Status |
|---|-----------|------|--------|
| §3.1 | AI-Native by Design | RAG chatbot with selected-text Q&A | PLANNED |
| §3.2 | Spec-Driven Development | All work traced to spec FR-xxx | PASS |
| §3.3 | Capstone-Driven Architecture | Book content builds to capstone | PASS (content exists) |
| §3.4 | Artifact-First Integrity | All code artifacts exist and are real | PASS (verified) |
| §3.5 | Resource-Constrained | CPU-only for book+RAG, no heavy GPU | PASS |
| §3.6 | Minimal Embeddings | 500–800 token chunks, Qdrant free tier | PLANNED |
| §3.7 | Hackathon Compliance | Docusaurus + RAG + deploy + demo | PLANNED |
| §7 | Architectural Separation | RAG backend vs Frontend separated | PLANNED |
| §9 | Security | Env vars only, no keys in repo | PLANNED |
| §11 | Non-Negotiable Rules | 4-module structure preserved | PASS |

**Gate result: PASS — no violations. Proceed to implementation.**

## Current State Assessment

### Already Complete

| Area | Status | Location |
|---|---|---|
| Book content (36 chapters) | Done | `docs/` (Docusaurus) |
| Module 1 code (ROS 2) | Done | `code/ros2/` |
| Module 2 world (Gazebo) | Done | `code/gazebo/` |
| Module 3 config (Nav2) | Done | `code/navigation/` |
| Module 4 code (VLA pipeline) | Done | `code/vla/` |
| Architecture diagrams | Done | `diagrams/` |
| Hardware specs + install script | Done | `hardware/` |
| Docusaurus config + sidebar | Done | `docs/docusaurus.config.js` |

### Needs to Be Built

| Area | Priority | Effort |
|---|---|---|
| FastAPI backend (RAG API) | P1 | Medium |
| Embedding pipeline (content → Qdrant) | P1 | Medium |
| Neon database schema (chat history) | P1 | Small |
| Chatbot React component | P1 | Medium |
| Selected-text Q&A integration | P1 | Medium |
| Docusaurus site cleanup (remove `my-website/`) | P1 | Small |
| Vercel deployment config | P1 | Small |
| Environment variable setup | P1 | Small |
| Demo video (≤ 90 seconds) | P2 | Small |
| Optional: Better-Auth | P3 | Medium |
| Optional: Personalization | P3 | Medium |
| Optional: Urdu translation | P3 | Medium |

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-book/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── api-spec.md      # RAG API endpoints
│   ├── artifact-registry.md
│   └── module-interfaces.md
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment variable management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat.py          # Chat request/response schemas
│   │   └── embedding.py     # Embedding metadata schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag.py           # RAG query orchestration
│   │   ├── embedder.py      # Text chunking + embedding
│   │   ├── qdrant.py        # Qdrant client wrapper
│   │   └── neon.py          # Neon/Postgres client wrapper
│   └── api/
│       ├── __init__.py
│       ├── chat.py          # POST /api/chat endpoint
│       ├── search.py        # POST /api/search endpoint
│       └── health.py        # GET /api/health endpoint
├── scripts/
│   └── embed_content.py     # One-time embedding pipeline script
├── requirements.txt
├── .env.example
└── tests/
    ├── test_rag.py
    └── test_embedder.py

docs/                        # Existing Docusaurus site (keep as-is)
├── docusaurus.config.js     # Update: add chatbot plugin/component
├── src/
│   ├── components/
│   │   ├── ChatBot/         # NEW: RAG chatbot React component
│   │   │   ├── index.tsx
│   │   │   ├── ChatBot.module.css
│   │   │   └── TextSelection.tsx
│   │   └── ...
│   ├── theme/
│   │   └── Root.tsx         # NEW: Wrap site with chatbot provider
│   └── css/
│       └── custom.css       # Update: chatbot styles
├── static/
└── docs/                    # Book content (already written)

code/                        # Existing code artifacts (no changes)
├── ros2/
├── gazebo/
├── navigation/
└── vla/
```

**Structure Decision**: Web application pattern with separated backend
(FastAPI) and frontend (Docusaurus). The `my-website/` directory is
unused boilerplate and should be removed. The `docs/` directory IS
the frontend. The `backend/` directory is new.

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│                    Vercel                         │
│  ┌─────────────────────────────────────────────┐ │
│  │  Docusaurus Static Site (docs/)             │ │
│  │  ┌──────────┐  ┌────────────────────────┐   │ │
│  │  │ Chapters │  │ ChatBot Component      │   │ │
│  │  │ (36 .md) │  │ - Free-form Q&A        │   │ │
│  │  │          │  │ - Selected-text Q&A     │   │ │
│  │  └──────────┘  └───────────┬────────────┘   │ │
│  └────────────────────────────┼────────────────┘ │
└───────────────────────────────┼──────────────────┘
                                │ HTTPS
                                ▼
┌──────────────────────────────────────────────────┐
│              Railway / Render                     │
│  ┌─────────────────────────────────────────────┐ │
│  │  FastAPI Backend (backend/)                 │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │ │
│  │  │ /api/chat│  │/api/search│  │/api/health│ │ │
│  │  └────┬─────┘  └────┬─────┘  └──────────┘  │ │
│  │       │              │                       │ │
│  │       ▼              ▼                       │ │
│  │  ┌──────────────────────────────────────┐   │ │
│  │  │  RAG Service                         │   │ │
│  │  │  - Query embedding                   │   │ │
│  │  │  - Qdrant vector search              │   │ │
│  │  │  - Context assembly                  │   │ │
│  │  │  - LLM answer generation             │   │ │
│  │  └──────┬───────────────┬───────────────┘   │ │
│  └─────────┼───────────────┼───────────────────┘ │
└────────────┼───────────────┼─────────────────────┘
             │               │
             ▼               ▼
     ┌──────────────┐ ┌──────────────┐
     │ Qdrant Cloud │ │ Neon Postgres│
     │ (Free Tier)  │ │ (Serverless) │
     │ - Embeddings │ │ - Chat logs  │
     │ - Metadata   │ │ - Sessions   │
     └──────────────┘ └──────────────┘
```

## Embedding Strategy (§3.6 Compliance)

| Parameter | Value | Rationale |
|---|---|---|
| Chunk size | 600 tokens (target) | Within 500–800 range, balances context |
| Overlap | 50 tokens | Minimal, prevents context loss at boundaries |
| Embedding model | `text-embedding-3-small` | Smallest OpenAI model, 1536 dims |
| Content scope | Canonical chapter text only | No duplicate code blocks, no boilerplate |
| Metadata | chapter, module, section, type | Enables filtered search without re-embedding |
| Estimated vectors | ~200–250 | Well within Qdrant Free Tier (1M vectors) |
| Re-embedding | Incremental only (hash-based) | Full re-embed prohibited by constitution |

## Deployment Strategy

| Component | Platform | Config |
|---|---|---|
| Docusaurus site | Vercel | Static build from `docs/` |
| FastAPI backend | Railway or Render | Docker container, auto-deploy from `backend/` |
| Qdrant | Qdrant Cloud | Free Tier cluster |
| Neon Postgres | Neon | Serverless, free tier |
| Secrets | Environment variables | `.env.example` in repo, real values in platform |

## Complexity Tracking

> No constitution violations detected. No complexity justifications needed.

| Item | Assessment |
|---|---|
| Book content | Already complete — no work needed |
| Code artifacts | Already complete — no work needed |
| Backend (new) | Standard FastAPI + vector search — low complexity |
| Frontend chatbot (new) | React component in Docusaurus — medium complexity |
| Deployment | Standard Vercel + Railway — low complexity |
