"""GET /api/health — service health check."""

from fastapi import APIRouter

from app.services import qdrant as qdrant_mod
from app.services.neon import neon_service

router = APIRouter()


@router.get("/health")
async def health_check():
    qdrant_ok = (
        qdrant_mod.qdrant_service.health_check()
        if qdrant_mod.qdrant_service
        else False
    )
    neon_ok = await neon_service.health_check()
    embedding_count = (
        qdrant_mod.qdrant_service.count() if qdrant_mod.qdrant_service else 0
    )

    status = "healthy" if (qdrant_ok and neon_ok) else "degraded"

    return {
        "status": status,
        "qdrant": "connected" if qdrant_ok else "disconnected",
        "neon": "connected" if neon_ok else "disconnected",
        "embedding_count": embedding_count,
    }
