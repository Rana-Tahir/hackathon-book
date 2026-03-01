# Data Model: Physical AI & Humanoid Robotics — AI-Native Textbook

**Phase**: 1 — Design & Contracts
**Date**: 2026-02-16 (updated from 2026-02-13)
**Feature**: 001-physical-ai-book
**Constitution**: v2.0.0

## Entity Definitions

### Module (Content Entity — Already Complete)

A self-contained instructional unit that teaches one domain of the
Physical AI stack. 4 modules exist, fully authored in `docs/`.

| ID | Title | Focus | Prerequisites |
|----|-------|-------|--------------|
| 1 | Foundations of Physical AI & ROS 2 | ROS 2 middleware | None |
| 2 | Simulation & Digital Twins | Gazebo physics simulation | Module 1 |
| 3 | Perception & Navigation | Isaac + Nav2 pipelines | Module 2 |
| 4 | Vision-Language-Action & Capstone | LLM-driven action | Module 3 |

### Artifact (Content Entity — Already Complete)

A concrete, runnable deliverable produced during a module. See
`contracts/artifact-registry.md` for full registry.

### Embedding (New — RAG System)

A vector representation of a chunk of book content stored in Qdrant.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | string (UUID) | Unique embedding identifier |
| content | string | Original text chunk (600 tokens target) |
| content_hash | string (MD5) | Hash for incremental update detection |
| vector | float[1536] | OpenAI text-embedding-3-small output |
| module | int (1–4) | Source module number |
| chapter | string | Source chapter filename |
| section | string | Source section heading |
| content_type | enum | "prose", "code", "table", "definition" |
| position | int | Sequential position within chapter |

**Constraints**:
- Chunk size: 500–800 tokens (target 600) per §3.6
- Overlap: 50 tokens between adjacent chunks
- No duplicate content embedded
- No unnecessary code blocks embedded
- Total vectors: ~200–250 (within Qdrant Free Tier)

### ChatSession (New — Neon Postgres)

An anonymous conversation session between a user and the RAG chatbot.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | string (UUID) | Session identifier |
| created_at | timestamp | Session creation time |
| updated_at | timestamp | Last activity time |

### ChatMessage (New — Neon Postgres)

A single message within a chat session.

| Attribute | Type | Description |
|-----------|------|-------------|
| id | serial | Auto-incrementing message ID |
| session_id | string (UUID) | FK to ChatSession |
| role | enum | "user" or "assistant" |
| content | text | Message content |
| selected_text | text (nullable) | Text selected by user on page |
| chapter | string (nullable) | Current chapter when asked |
| module | int (nullable) | Current module when asked |
| created_at | timestamp | Message timestamp |

### Capstone (Content Entity — Already Complete)

Integrative project composing all module artifacts. Documented in
`docs/capstone/`.

### Hardware Profile (Content Entity — Already Complete)

Documented hardware configurations. See `hardware/requirements.md`.

## Entity Relationships

```text
Module 1..4 ──produces──→ Artifacts
Module 1..4 ──chunks-into──→ Embeddings (via embedding pipeline)
Embeddings ──stored-in──→ Qdrant Cloud
ChatSession ──has-many──→ ChatMessage
ChatMessage ──references──→ Module (nullable)
ChatMessage ──references──→ Chapter (nullable)
ChatSession ──stored-in──→ Neon Postgres
```

## Database Schema (Neon Postgres)

```sql
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    selected_text TEXT,
    chapter VARCHAR(100),
    module INTEGER CHECK (module BETWEEN 1 AND 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_messages_session ON chat_messages(session_id);
CREATE INDEX idx_messages_chapter ON chat_messages(chapter);
```

## Qdrant Collection Schema

```json
{
  "collection_name": "book_content",
  "vectors": {
    "size": 1536,
    "distance": "Cosine"
  },
  "payload_schema": {
    "module": "integer",
    "chapter": "keyword",
    "section": "keyword",
    "content_type": "keyword",
    "content_hash": "keyword",
    "position": "integer"
  }
}
```

## State Transitions

### Embedding Pipeline

```text
MARKDOWN_FILE → CHUNK → HASH_CHECK → EMBED (if new/changed) → UPSERT_QDRANT
```

### Chat Flow

```text
USER_QUERY → EMBED_QUERY → QDRANT_SEARCH → CONTEXT_ASSEMBLY → LLM_ANSWER → STORE_MESSAGE
```
