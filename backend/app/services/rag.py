"""RAG query orchestration service (§3.1 compliant — book-only grounding)."""

from openai import OpenAI

from app.config import settings
from app.services import qdrant as qdrant_mod

SYSTEM_PROMPT = """You are the AI assistant for the Physical AI & Humanoid Robotics textbook.

STRICT RULES:
1. Answer ONLY from the provided book content context below.
2. If the context does not contain the answer, say: "I don't have information about that in the book content. Please try asking about a topic covered in the modules."
3. NEVER speculate about robotics APIs, hardware capabilities, or ROS 2 features not mentioned in the context.
4. NEVER generate ROS 2 commands not documented in the book.
5. Always cite which chapter/section your answer comes from.
6. Keep answers concise and educational.

BOOK CONTEXT:
{context}
"""

SELECTED_TEXT_PROMPT = """The user has selected this text from the book:
---
{selected_text}
---

Answer their question about this specific passage, using the broader context provided."""


class RAGService:
    """Orchestrates query embedding, vector search, and LLM answer generation."""

    def __init__(self) -> None:
        self.openai = OpenAI(api_key=settings.openai_api_key)

    def _embed_query(self, query: str) -> list[float]:
        """Embed a user query using text-embedding-3-small."""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=query,
        )
        return response.data[0].embedding

    def search(
        self,
        query: str,
        limit: int = 5,
        module: int | None = None,
        chapter: str | None = None,
    ) -> list[dict]:
        """Search Qdrant for relevant book content."""
        query_vector = self._embed_query(query)
        return qdrant_mod.qdrant_service.search(
            query_vector=query_vector,
            limit=limit,
            module=module,
            chapter=chapter,
        )

    def answer(
        self,
        message: str,
        selected_text: str | None = None,
        chapter: str | None = None,
        module: int | None = None,
        history: list[dict] | None = None,
    ) -> tuple[str, list[dict]]:
        """Generate a grounded answer from book content.

        Returns (answer_text, source_references).
        """
        # Search with chapter boost if selected text provided
        search_chapter = chapter if selected_text else None
        results = self.search(
            query=message,
            limit=5,
            module=module,
            chapter=search_chapter,
        )

        if not results:
            return (
                "I don't have information about that in the book content. "
                "Please try asking about a topic covered in the modules.",
                [],
            )

        # Build context from search results
        context_parts = []
        for r in results:
            context_parts.append(
                f"[{r['chapter']} — {r['section']}]\n{r['content']}"
            )
        context = "\n\n---\n\n".join(context_parts)

        # Build messages
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        ]

        # Add conversation history if available
        if history:
            for msg in history[-4:]:  # Last 4 messages for context
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add selected text context if provided
        user_content = message
        if selected_text:
            user_content = (
                SELECTED_TEXT_PROMPT.format(selected_text=selected_text)
                + "\n\nQuestion: "
                + message
            )

        messages.append({"role": "user", "content": user_content})

        # Call LLM
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=800,
        )

        answer = response.choices[0].message.content

        # Format sources
        sources = [
            {
                "chapter": r["chapter"],
                "section": r["section"],
                "relevance": r["relevance"],
            }
            for r in results[:3]  # Top 3 sources
        ]

        return answer, sources


# Module-level singleton
rag_service = RAGService()
