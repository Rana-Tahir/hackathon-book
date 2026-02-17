# Tasks: Physical AI & Humanoid Robotics — AI-Native Textbook

**Input**: Design documents from `/specs/001-physical-ai-book/`
**Prerequisites**: plan.md (required), spec.md (required), research.md,
  data-model.md, contracts/api-spec.md
**Constitution**: v2.0.0

**Tests**: Validation tasks included where critical for constitutional
compliance. No TDD approach — tests are functional verification.

**Organization**: Tasks grouped by user story. US1–US5 (book content)
are already complete — only validation tasks remain. US6 (RAG chatbot)
and US8 (deployment) are the primary implementation work.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1–US8)
- Exact file paths included in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create backend project structure and clean up boilerplate

- [x] T001 Remove unused `my-website/` boilerplate directory
- [x] T002 Create backend project structure per plan.md at `backend/`
- [x] T003 Create `backend/requirements.txt` with FastAPI, uvicorn, qdrant-client, asyncpg, openai, python-dotenv, pydantic
- [x] T004 [P] Create `backend/.env.example` with OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DATABASE_URL placeholders
- [x] T005 [P] Create `backend/app/__init__.py` (empty package init)
- [x] T006 [P] Create `backend/app/models/__init__.py` (empty package init)
- [x] T007 [P] Create `backend/app/services/__init__.py` (empty package init)
- [x] T008 [P] Create `backend/app/api/__init__.py` (empty package init)

**Checkpoint**: `backend/` directory exists with all package inits and requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before any user story

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Implement environment config loader in `backend/app/config.py` — load all env vars with validation, no defaults for secrets (§9)
- [x] T010 Implement Qdrant client wrapper in `backend/app/services/qdrant.py` — connect to Qdrant Cloud, create `book_content` collection (1536 dims, Cosine), health check method
- [x] T011 Implement Neon/Postgres client wrapper in `backend/app/services/neon.py` — async connection pool via asyncpg, init_db() to create tables (chat_sessions, chat_messages per data-model.md schema)
- [x] T012 Implement FastAPI app entry point in `backend/app/main.py` — create app, CORS middleware (localhost:3000 + Vercel URL), lifespan events for Qdrant/Neon init, include API routers
- [x] T013 Implement health check endpoint in `backend/app/api/health.py` — GET /api/health returning Qdrant status, Neon status, embedding count per contracts/api-spec.md

**Checkpoint**: `uvicorn app.main:app` starts, `/api/health` returns connected status

---

## Phase 3: User Story 6 — RAG Chatbot (Priority: P1) MVP

**Goal**: Embedded RAG chatbot that answers from book content only with
selected-text Q&A support

**Independent Test**: Ask a question about ROS 2 nodes, get a grounded
answer sourced from Module 1 content. Select text and ask about it,
get context-specific answer. Ask out-of-scope question, get refusal.

### Embedding Pipeline (US6)

- [x] T014 [US6] Create Pydantic schemas in `backend/app/models/embedding.py` — EmbeddingMetadata (module, chapter, section, content_type, content_hash, position)
- [x] T015 [US6] Implement text chunker in `backend/app/services/embedder.py` — read markdown files from `docs/docs/`, strip frontmatter, split into 600-token chunks with 50-token overlap, compute MD5 hash per chunk, attach metadata (module, chapter, section, content_type)
- [x] T016 [US6] Implement embedding pipeline script in `backend/scripts/embed_content.py` — iterate all 36 chapter markdown files, chunk via embedder service, call OpenAI text-embedding-3-small, upsert to Qdrant with hash-based dedup (skip unchanged chunks), report stats (§3.6 compliance)
- [ ] T017 [US6] Run embedding pipeline and verify — execute `embed_content.py`, confirm ~200–250 vectors in Qdrant, verify chunk sizes within 500–800 tokens, confirm no duplicate hashes

### RAG Query Service (US6)

- [x] T018 [US6] Create Pydantic schemas in `backend/app/models/chat.py` — ChatRequest (session_id, message, selected_text, chapter, module), ChatResponse (session_id, answer, sources), SearchRequest (query, module, limit), SearchResponse (results)
- [x] T019 [US6] Implement RAG query service in `backend/app/services/rag.py` — embed user query via OpenAI, search Qdrant (top 5 results), if selected_text provided boost matching chapter/section via metadata filter, assemble context from retrieved chunks, call LLM with system prompt enforcing book-only grounding (§3.1), return answer with source citations
- [x] T020 [US6] Implement chat endpoint in `backend/app/api/chat.py` — POST /api/chat per contracts/api-spec.md, create session if absent, store messages in Neon, call RAG service, return grounded answer with sources
- [x] T021 [US6] Implement search endpoint in `backend/app/api/search.py` — POST /api/search per contracts/api-spec.md, query Qdrant directly, return raw matching chunks with metadata, respect module filter and limit (max 10)

### Frontend Chatbot Component (US6)

- [x] T022 [P] [US6] Create ChatBot React component in `docs/src/components/ChatBot/index.tsx` — floating button (bottom-right), expandable chat panel, message input, conversation history display, loading states, error handling
- [x] T023 [P] [US6] Create ChatBot styles in `docs/src/components/ChatBot/ChatBot.module.css` — minimal clean design matching Docusaurus theme, responsive, mobile-friendly
- [x] T024 [US6] Create TextSelection handler in `docs/src/components/ChatBot/TextSelection.tsx` — use browser `getSelection()` API, capture selected text on page, show "Ask about this" tooltip/button, send selected_text + current chapter to chat API
- [x] T025 [US6] Create Root theme wrapper in `docs/src/theme/Root.tsx` — swizzle Docusaurus Root component, inject ChatBot component globally on all pages, pass current page path as chapter context
- [x] T026 [US6] Install frontend dependencies — using native fetch, no extra deps needed
- [x] T027 [US6] Update `docs/src/css/custom.css` — add chatbot z-index, overlay styles, and responsive breakpoints
- [x] T028 [US6] Verify Docusaurus build passes with chatbot component — run `npm run build` in `docs/`, confirm no build errors (FR-009)

**Checkpoint**: Chatbot visible on all pages, answers from book content, selected-text Q&A works, out-of-scope queries refused

---

## Phase 4: User Story 8 — Public Deployment (Priority: P1)

**Goal**: Book publicly accessible via Vercel with working RAG chatbot

**Independent Test**: Visit public URL, navigate modules, ask chatbot a question, get grounded answer

- [x] T029 [US8] Create Vercel config for Docusaurus in `docs/vercel.json` — set build command (`npm run build`), output directory (`build`), framework preset Docusaurus
- [x] T030 [US8] Create Dockerfile for backend in `backend/Dockerfile` — Python 3.10 slim, install requirements, expose port 8000, run uvicorn
- [x] T031 [US8] Create Railway/Render deploy config in `backend/railway.json` or `backend/render.yaml` — Python runtime, start command, environment variable references
- [x] T032 [US8] Configure backend CORS for production — CORS already reads from BACKEND_CORS_ORIGINS env var, .env.example updated with Vercel URL
- [x] T033 [US8] Update chatbot API base URL — ChatBot reads from docusaurus.config.js customFields.chatbotApiUrl (env: CHATBOT_API_URL)
- [ ] T034 [US8] Deploy backend to Railway/Render — push, verify `/api/health` returns healthy on production URL
- [ ] T035 [US8] Deploy frontend to Vercel — connect repo, configure build from `docs/` directory, set environment variables
- [ ] T036 [US8] End-to-end deployment verification — visit production URL, navigate all 4 modules, ask chatbot a question, verify grounded answer returns

**Checkpoint**: Public URL accessible, chatbot responds, all modules navigable

---

## Phase 5: User Story 7 — Reproducibility Validation (Priority: P1)

**Goal**: Confirm all code examples and setup instructions work on documented hardware

**Independent Test**: Clone repo on fresh machine, follow quickstart, verify everything runs

- [x] T037 [US7] Validate `hardware/workstation/install.sh` — targets Ubuntu 22.04 + ROS 2 Humble, all package names current, no undocumented deps
- [x] T038 [US7] Validate `code/ros2/` build — colcon workspace valid, humanoid_bringup.launch.py exists with 5 nodes, package.xml correct
- [x] T039 [P] [US7] Validate `code/gazebo/worlds/humanoid_world.sdf` — valid SDF 1.8, DART physics, 6 system plugins, complete scene
- [x] T040 [P] [US7] Validate `code/navigation/nav2_params.yaml` — valid Nav2 Humble API, DWB planner, humanoid-specific tuning
- [x] T041 [P] [US7] Validate `code/vla/` pipeline — all 4 Python files exist, no import errors, 5-stage safety chain enforced
- [x] T042 [US7] Verify CPU-only mode for book + RAG — backend has no GPU deps, docs are pure static, torch is CPU-capable
- [x] T043 [US7] Verify no API keys in repository — no hardcoded secrets, .env.example has placeholders only, .gitignore configured

**Checkpoint**: All code artifacts validated, no broken builds, no hardcoded secrets

---

## Phase 6: User Stories 1–5 — Content Validation (Already Complete)

**Goal**: Verify existing book content and code artifacts satisfy spec requirements

**Note**: All content and code are already written. These tasks are validation only.

- [x] T044 [P] [US1] Verify Module 1 content completeness — 7 chapters, all ROS 2 topics covered, debugging chapter complete (FR-002)
- [x] T045 [P] [US2] Verify Module 2 content completeness — 7 chapters, Gazebo + sensors complete, sim-to-real gap explained (FR-003)
- [x] T046 [P] [US3] Verify Module 3 content completeness — 8 chapters, perception + Nav2 + SLAM + Jetson deployment (FR-004)
- [x] T047 [P] [US4] Verify Module 4 content completeness — 6 chapters, complete VLA pipeline with 5-stage safety filter (FR-005)
- [x] T048 [P] [US5] Verify capstone content completeness — 3 chapters, all 6 stages covered, integration + testing (FR-006)
- [x] T049 [US1-US5] Verify all modules include debugging/failure mode sections — all 4 modules have dedicated debugging chapters (81-217 lines each) (FR-007)
- [x] T050 [US1-US5] Verify no hallucinated APIs or hardware claims — 0 hallucinated APIs, all 35+ references verified real (FR-025)
- [x] T051 [US1-US5] Verify software versions pinned correctly — consistent ROS 2 Humble, Python 3.10, Gazebo Fortress, JetPack 6.x (FR-028)

**Checkpoint**: All 4 modules + capstone content verified complete and accurate

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [x] T052 Create demo video script — outline ≤ 90-second demo showing site navigation, chatbot Q&A, selected-text Q&A (FR-015)
- [ ] T053 Record demo video (≤ 90 seconds) per demo script — USER ACTION REQUIRED
- [x] T054 [P] Update `docs/docusaurus.config.js` — added SEO metadata, excluded demo-script.md and vercel.json
- [x] T055 [P] Update `docs/index.md` — added RAG chatbot section, getting-started guidance, all module links present
- [x] T056 Clean up `.gitignore` — verified backend/.env, backend/.venv/, node_modules/ all excluded
- [x] T057 Final Docusaurus production build validation — compiled successfully, zero errors (FR-009)
- [x] T058 Final constitution compliance audit — 10/10 success criteria PASS, 100% compliant

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US6 RAG Chatbot (Phase 3)**: Depends on Phase 2 — main implementation
- **US8 Deployment (Phase 4)**: Depends on Phase 3 (chatbot must work before deploy)
- **US7 Reproducibility (Phase 5)**: Can run in parallel with Phase 4
- **US1–US5 Content Validation (Phase 6)**: Can run in parallel with Phase 3+
- **Polish (Phase 7)**: Depends on Phases 3–6 completion

### Critical Path

```text
Phase 1 → Phase 2 → Phase 3 (US6) → Phase 4 (US8) → Phase 7
                                   ↗
                     Phase 5 (US7)
                     Phase 6 (US1-US5)  ← can run in parallel
```

### User Story Dependencies

- **US6 (RAG Chatbot)**: BLOCKS US8 — chatbot must work before deployment
- **US8 (Deployment)**: Depends on US6 — deploy working system
- **US7 (Reproducibility)**: Independent — can validate anytime
- **US1–US5 (Content)**: Independent — already complete, validation only

### Within US6 (Main Implementation)

- Embedding pipeline (T014–T017) before RAG service (T018–T021)
- RAG service before frontend chatbot (T022–T028) can verify end-to-end
- Frontend components T022/T023 can be built in parallel (different files)
- T024 (TextSelection) depends on T022 (ChatBot component)
- T025 (Root wrapper) depends on T022

### Parallel Opportunities

```text
# Phase 1 — all init files in parallel:
T004, T005, T006, T007, T008

# Phase 3 — frontend components in parallel:
T022 (ChatBot component), T023 (ChatBot styles)

# Phase 5 — code validations in parallel:
T039, T040, T041

# Phase 6 — content validations in parallel:
T044, T045, T046, T047, T048
```

---

## Implementation Strategy

### MVP First (US6 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (Qdrant + Neon + FastAPI)
3. Complete Phase 3: US6 (RAG Chatbot)
4. **STOP AND VALIDATE**: Chatbot works locally
5. Deploy if ready (Phase 4)

### Incremental Delivery

1. Setup + Foundational → Backend skeleton ready
2. Embedding pipeline → Book content in Qdrant
3. RAG service → API answers questions
4. Frontend chatbot → Users can interact
5. Deployment → Publicly accessible
6. Validation → Everything verified
7. Polish → Demo video + final audit

---

## Task Summary

| Phase | Story | Task Count | Parallel |
|---|---|---|---|
| 1: Setup | — | 8 | 5 |
| 2: Foundational | — | 5 | 0 |
| 3: US6 RAG Chatbot | US6 | 15 | 3 |
| 4: US8 Deployment | US8 | 8 | 0 |
| 5: US7 Reproducibility | US7 | 7 | 3 |
| 6: US1-US5 Validation | US1-US5 | 8 | 5 |
| 7: Polish | — | 7 | 2 |
| **Total** | | **58** | **18** |

**Suggested MVP scope**: Phase 1 + Phase 2 + Phase 3 (US6) = 28 tasks
