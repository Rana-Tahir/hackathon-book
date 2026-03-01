"""FastAPI application entry point for the RAG chatbot backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.services.qdrant import QdrantService, qdrant_service as _qs
from app.services import qdrant as qdrant_mod
from app.services.neon import neon_service
from app.api import health, chat, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and tear down services."""
    # Startup
    svc = QdrantService(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    svc.ensure_collection()
    qdrant_mod.qdrant_service = svc

    await neon_service.connect(settings.neon_database_url)

    yield

    # Shutdown
    await neon_service.close()


app = FastAPI(
    title="Physical AI Book — RAG Chatbot API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(search.router, prefix="/api")
