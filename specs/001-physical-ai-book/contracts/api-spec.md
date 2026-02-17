# API Specification: RAG Chatbot Backend

**Date**: 2026-02-16
**Feature**: 001-physical-ai-book
**Base URL**: `https://<backend-host>/api`

## Endpoints

### POST /api/chat

Send a user message and receive a RAG-grounded answer.

**Request**:
```json
{
  "session_id": "uuid (optional — created if absent)",
  "message": "What is a ROS 2 node?",
  "selected_text": "A node is the fundamental...",
  "chapter": "module-1/02-nodes-topics",
  "module": 1
}
```

**Response** (200):
```json
{
  "session_id": "uuid",
  "answer": "Based on the book content, a ROS 2 node is...",
  "sources": [
    {
      "chapter": "module-1/02-nodes-topics",
      "section": "What is a Node?",
      "relevance": 0.92
    }
  ]
}
```

**Response** (422): Validation error
**Response** (503): Qdrant/Neon unavailable

**Behavior**:
- If `selected_text` is provided, boost search results from that
  chapter/section.
- If `session_id` is absent, create a new session.
- Answer MUST be grounded in book content only (§3.1, FR-013).
- If question is out of scope, respond with a refusal message.

---

### POST /api/search

Search book content without LLM answer generation. Returns raw
matching chunks.

**Request**:
```json
{
  "query": "Nav2 obstacle avoidance",
  "module": 3,
  "limit": 5
}
```

**Response** (200):
```json
{
  "results": [
    {
      "content": "Nav2 uses the DWB controller for...",
      "chapter": "module-3/05-nav2-setup",
      "section": "Obstacle Avoidance",
      "relevance": 0.89
    }
  ]
}
```

**Behavior**:
- `module` filter is optional — narrows search to specific module.
- `limit` defaults to 5, max 10.
- Uses Qdrant vector similarity search.

---

### GET /api/health

Health check for monitoring and deployment verification.

**Response** (200):
```json
{
  "status": "healthy",
  "qdrant": "connected",
  "neon": "connected",
  "embedding_count": 237
}
```

**Response** (503):
```json
{
  "status": "degraded",
  "qdrant": "disconnected",
  "neon": "connected",
  "error": "Qdrant connection timeout"
}
```

## Authentication

None required for base functionality. All endpoints are public.
If Better-Auth bonus feature is implemented, session-based auth
can be added as middleware.

## Rate Limiting

- `/api/chat`: 30 requests/minute per session
- `/api/search`: 60 requests/minute per session
- `/api/health`: No limit

## CORS

- Allow origins: Vercel deployment URL, `localhost:3000`
- Allow methods: GET, POST, OPTIONS
- Allow headers: Content-Type

## Error Taxonomy

| Code | Meaning | When |
|------|---------|------|
| 200 | Success | Normal response |
| 400 | Bad Request | Malformed JSON |
| 422 | Validation Error | Missing required fields |
| 429 | Rate Limited | Too many requests |
| 503 | Service Unavailable | Qdrant/Neon down |
