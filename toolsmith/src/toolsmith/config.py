"""Settings, loaded from environment / .env."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="TOOLSMITH_",
        extra="ignore",
    )

    # --- Model ---
    base_model: str = "Qwen/Qwen2.5-0.5B-Instruct"
    output_dir: Path = Path("./outputs")

    # --- LoRA hyperparams ---
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: list[str] = Field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj"]
    )

    # --- Training ---
    lr: float = 2e-4
    epochs: int = 3
    batch_size: int = 4
    grad_accum: int = 4
    max_seq_length: int = 1024
    warmup_ratio: float = 0.03
    seed: int = 42

    # --- Data ---
    data_dir: Path = Path("./data")


settings = Settings()
