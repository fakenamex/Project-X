from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from .models import DailyReport, PublishedArticle


class Repository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self) -> None:
        with self._connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    category TEXT NOT NULL,
                    published_at TEXT NOT NULL
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    improvements TEXT NOT NULL
                )
                """
            )

    def save_article(self, article: PublishedArticle) -> int:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO articles(title, body, category, published_at) VALUES (?, ?, ?, ?)",
                (article.title, article.body, article.category, article.published_at.isoformat()),
            )
            return int(cur.lastrowid)

    def list_recent_articles(self, limit: int = 20) -> list[PublishedArticle]:
        with self._connect() as con:
            rows = con.execute(
                "SELECT id, title, body, category, published_at FROM articles ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            PublishedArticle(
                id=row[0],
                title=row[1],
                body=row[2],
                category=row[3],
                published_at=datetime.fromisoformat(row[4]),
            )
            for row in rows
        ]

    def save_daily_report(self, report: DailyReport) -> None:
        with self._connect() as con:
            con.execute(
                "INSERT INTO daily_reports(created_at, summary, improvements) VALUES (?, ?, ?)",
                (report.created_at.isoformat(), report.summary, "\n".join(report.proposed_improvements)),
            )
