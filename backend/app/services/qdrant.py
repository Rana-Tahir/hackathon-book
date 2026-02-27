"""Qdrant Cloud client wrapper for book content vectors."""

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
)

COLLECTION_NAME = "book_content"
VECTOR_SIZE = 384  # fastembed BAAI/bge-small-en-v1.5


class QdrantService:
    """Manages connection and operations against Qdrant Cloud."""

    def __init__(self, url: str, api_key: str) -> None:
        self.client = QdrantClient(url=url, api_key=api_key)

    def ensure_collection(self) -> None:
        """Create the book_content collection if it doesn't exist."""
        collections = [c.name for c in self.client.get_collections().collections]
        if COLLECTION_NAME not in collections:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE, distance=Distance.COSINE
                ),
            )

    def upsert_points(self, points: list[PointStruct]) -> None:
        """Upsert embedding points into the collection."""
        self.client.upsert(collection_name=COLLECTION_NAME, points=points)

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
        module: int | None = None,
        chapter: str | None = None,
    ) -> list[dict]:
        """Search for similar content chunks with optional filters."""
        conditions = []
        if module is not None:
            conditions.append(
                FieldCondition(key="module", match=MatchValue(value=module))
            )
        if chapter is not None:
            conditions.append(
                FieldCondition(key="chapter", match=MatchValue(value=chapter))
            )

        query_filter = Filter(must=conditions) if conditions else None

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter,
            with_payload=True,
        )

        return [
            {
                "content": hit.payload.get("content", ""),
                "chapter": hit.payload.get("chapter", ""),
                "section": hit.payload.get("section", ""),
                "module": hit.payload.get("module", 0),
                "relevance": round(hit.score, 3),
            }
            for hit in results
        ]

    def count(self) -> int:
        """Return the number of vectors in the collection."""
        try:
            info = self.client.get_collection(COLLECTION_NAME)
            return info.points_count or 0
        except Exception:
            return 0

    def health_check(self) -> bool:
        """Check if Qdrant is reachable."""
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False


# Module-level singleton, initialized in app lifespan
qdrant_service: QdrantService | None = None
