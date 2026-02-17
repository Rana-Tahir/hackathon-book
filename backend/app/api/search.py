"""POST /api/search — direct vector search endpoint per contracts/api-spec.md."""

from fastapi import APIRouter

from app.models.chat import SearchRequest, SearchResponse, SearchResult
from app.services.rag import rag_service

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search_content(request: SearchRequest):
    results = rag_service.search(
        query=request.query,
        limit=request.limit,
        module=request.module,
    )

    return SearchResponse(
        results=[
            SearchResult(
                content=r["content"],
                chapter=r["chapter"],
                section=r["section"],
                relevance=r["relevance"],
            )
            for r in results
        ]
    )
