"""Neon Serverless Postgres client wrapper for chat history."""

import uuid

import asyncpg

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    selected_text TEXT,
    chapter VARCHAR(100),
    module INTEGER CHECK (module IS NULL OR module BETWEEN 1 AND 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_session ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_chapter ON chat_messages(chapter);
"""


class NeonService:
    """Manages async connection pool and chat persistence."""

    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    async def connect(self, database_url: str) -> None:
        """Create connection pool and initialize tables."""
        self.pool = await asyncpg.create_pool(database_url, min_size=1, max_size=5)
        async with self.pool.acquire() as conn:
            await conn.execute(CREATE_TABLES_SQL)

    async def close(self) -> None:
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()

    async def create_session(self) -> str:
        """Create a new chat session and return its ID."""
        session_id = str(uuid.uuid4())
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO chat_sessions (id) VALUES ($1)", uuid.UUID(session_id)
            )
        return session_id

    async def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id FROM chat_sessions WHERE id = $1",
                uuid.UUID(session_id),
            )
            return row is not None

    async def store_message(
        self,
        session_id: str,
        role: str,
        content: str,
        selected_text: str | None = None,
        chapter: str | None = None,
        module: int | None = None,
    ) -> None:
        """Store a chat message."""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO chat_messages
                   (session_id, role, content, selected_text, chapter, module)
                   VALUES ($1, $2, $3, $4, $5, $6)""",
                uuid.UUID(session_id),
                role,
                content,
                selected_text,
                chapter,
                module,
            )
            await conn.execute(
                "UPDATE chat_sessions SET updated_at = NOW() WHERE id = $1",
                uuid.UUID(session_id),
            )

    async def get_session_messages(
        self, session_id: str, limit: int = 10
    ) -> list[dict]:
        """Get recent messages for a session."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """SELECT role, content, selected_text, chapter, module, created_at
                   FROM chat_messages
                   WHERE session_id = $1
                   ORDER BY created_at DESC
                   LIMIT $2""",
                uuid.UUID(session_id),
                limit,
            )
            return [
                {
                    "role": r["role"],
                    "content": r["content"],
                    "selected_text": r["selected_text"],
                    "chapter": r["chapter"],
                    "module": r["module"],
                }
                for r in reversed(rows)
            ]

    async def health_check(self) -> bool:
        """Check if Neon is reachable."""
        try:
            async with self.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            return False


# Module-level singleton
neon_service = NeonService()
