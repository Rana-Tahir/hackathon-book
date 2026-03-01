"""Pydantic schemas for chat request/response per contracts/api-spec.md."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str
    selected_text: str | None = None
    chapter: str | None = None
    module: int | None = Field(None, ge=1, le=4)


class SourceReference(BaseModel):
    chapter: str
    section: str
    relevance: float


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[SourceReference]


class SearchRequest(BaseModel):
    query: str
    module: int | None = Field(None, ge=1, le=4)
    limit: int = Field(5, ge=1, le=10)


class SearchResult(BaseModel):
    content: str
    chapter: str
    section: str
    relevance: float


class SearchResponse(BaseModel):
    results: list[SearchResult]
