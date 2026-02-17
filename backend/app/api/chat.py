"""POST /api/chat — RAG-grounded chat endpoint per contracts/api-spec.md."""

from fastapi import APIRouter, HTTPException

from app.models.chat import ChatRequest, ChatResponse, SourceReference
from app.services.rag import rag_service
from app.services.neon import neon_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Resolve or create session
    session_id = request.session_id
    if session_id:
        if not await neon_service.session_exists(session_id):
            raise HTTPException(status_code=422, detail="Invalid session_id")
    else:
        session_id = await neon_service.create_session()

    # Store user message
    await neon_service.store_message(
        session_id=session_id,
        role="user",
        content=request.message,
        selected_text=request.selected_text,
        chapter=request.chapter,
        module=request.module,
    )

    # Get conversation history for context
    history = await neon_service.get_session_messages(session_id, limit=6)

    # Generate RAG answer
    answer, sources = rag_service.answer(
        message=request.message,
        selected_text=request.selected_text,
        chapter=request.chapter,
        module=request.module,
        history=history[:-1],  # Exclude the message we just stored
    )

    # Store assistant response
    await neon_service.store_message(
        session_id=session_id,
        role="assistant",
        content=answer,
        chapter=request.chapter,
        module=request.module,
    )

    return ChatResponse(
        session_id=session_id,
        answer=answer,
        sources=[
            SourceReference(
                chapter=s["chapter"],
                section=s["section"],
                relevance=s["relevance"],
            )
            for s in sources
        ],
    )
