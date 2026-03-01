"""Pydantic schemas for embedding metadata."""

from pydantic import BaseModel


class EmbeddingMetadata(BaseModel):
    """Metadata attached to each embedded chunk in Qdrant."""

    module: int
    chapter: str
    section: str
    content_type: str  # "prose", "code", "table", "definition"
    content_hash: str  # MD5 hash for incremental update detection
    position: int  # Sequential position within chapter


class EmbeddingChunk(BaseModel):
    """A chunk of book content ready for embedding."""

    content: str
    metadata: EmbeddingMetadata
