"""Application configuration loaded from environment / .env file.

We use pydantic-settings so settings are typed, validated, and discoverable.
Override any field with an environment variable prefixed with `READROVER_`.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for ReadRover."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="READROVER_",
        extra="ignore",
    )

    # --- LLM ---
    model: str = Field(
        default="claude-3-5-sonnet-latest",
        description="LangChain-compatible chat model identifier",
    )
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=64)

    # --- Retrieval ---
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    chroma_path: str = Field(default="./chroma_db")
    top_k_papers: int = Field(default=5, ge=1, le=20)
    top_k_chunks: int = Field(default=8, ge=1, le=50)
    chunk_size: int = Field(default=1000, ge=100)
    chunk_overlap: int = Field(default=150, ge=0)

    # --- Agentic loop ---
    max_iterations: int = Field(
        default=2,
        description="Max times the critic can re-trigger the search planner",
        ge=1,
        le=5,
    )

    # --- Logging ---
    log_level: str = Field(default="INFO")


settings = Settings()
