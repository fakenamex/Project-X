from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class NewsSignal:
    topic: str
    source: str
    summary: str


@dataclass
class ArticleDraft:
    title: str
    body: str
    category: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PublishedArticle:
    id: int | None
    title: str
    body: str
    category: str
    published_at: datetime


@dataclass
class DailyReport:
    created_at: datetime
    proposed_improvements: list[str]
    summary: str
