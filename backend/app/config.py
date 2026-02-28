"""Environment configuration loader. No defaults for secrets (§9)."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.groq_api_key: str = self._require("GROQ_API_KEY")
        self.qdrant_url: str = self._require("QDRANT_URL")
        self.qdrant_api_key: str = self._require("QDRANT_API_KEY")
        self.neon_database_url: str = self._require("NEON_DATABASE_URL")
        self.cors_origins: list[str] = os.getenv(
            "BACKEND_CORS_ORIGINS", "http://localhost:3000"
        ).split(",")

    @staticmethod
    def _require(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {name}")
        return value


settings = Settings()
