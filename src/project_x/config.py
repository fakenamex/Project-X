from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    db_path: Path = Path("projectx.db")
    host: str = "0.0.0.0"
    port: int = 8080
    cycle_interval_seconds: int = 24 * 60 * 60
    min_articles_per_day: int = 10


SETTINGS = Settings()
