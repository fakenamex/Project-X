from __future__ import annotations

from datetime import datetime

from .base import AgentContext
from ..models import ArticleDraft, DailyReport, NewsSignal, PublishedArticle


class FrontendDeveloperAgent:
    name = "KI Agent 1"
    specialty = "Frontend"

    def run(self, ctx: AgentContext) -> None:
        ctx.state["ui_note"] = "Homepage mit klaren Kategorien und Artikelkarten bereitgestellt."


class BackendDeveloperAgent:
    name = "KI Agent 2"
    specialty = "Backend"

    def run(self, ctx: AgentContext) -> None:
        ctx.state["api_note"] = "API liefert Artikel, Reports und Status für Dashboard."


class ResearchSpecialistAgent:
    name = "KI Agent 3"
    specialty = "Research"

    def run(self, ctx: AgentContext) -> None:
        signals: list[NewsSignal] = [
            NewsSignal(topic=f"Top-Thema {idx}", source="DE-News-Monitor", summary=f"Kurzanalyse zu Thema {idx}")
            for idx in range(1, 13)
        ]
        ctx.state["signals"] = signals


class TextWriterAgent:
    name = "KI Agent 4"
    specialty = "Writing"

    def run(self, ctx: AgentContext) -> None:
        signals: list[NewsSignal] = ctx.state.get("signals", [])
        drafts = [
            ArticleDraft(
                title=f"Analyse: {signal.topic}",
                body=(
                    f"Einordnung: {signal.summary}. "
                    "Bewertung der gesellschaftlichen Auswirkungen und wirtschaftlichen Relevanz."
                ),
                category="Analyse",
                metadata={"source": signal.source},
            )
            for signal in signals
        ]
        ctx.state["drafts"] = drafts


class PublisherAgent:
    name = "KI Agent 5"
    specialty = "Publishing"

    def run(self, ctx: AgentContext) -> None:
        drafts: list[ArticleDraft] = ctx.state.get("approved_drafts", [])
        published = [
            PublishedArticle(
                id=None,
                title=draft.title,
                body=draft.body,
                category=draft.category,
                published_at=datetime.utcnow(),
            )
            for draft in drafts
        ]
        ctx.state["published"] = published


class QualityManagerAgent:
    name = "KI Agent 6"
    specialty = "Quality & EU Compliance"

    forbidden_patterns = ["hate speech", "disinformation", "personal data"]

    def run(self, ctx: AgentContext) -> None:
        drafts: list[ArticleDraft] = ctx.state.get("drafts", [])
        approved: list[ArticleDraft] = []
        for draft in drafts:
            body_lower = draft.body.lower()
            if any(pattern in body_lower for pattern in self.forbidden_patterns):
                continue
            draft.metadata["eu_compliance_checked"] = True
            approved.append(draft)
        ctx.state["approved_drafts"] = approved


class MarketingManagerAgent:
    name = "KI Agent 7"
    specialty = "Marketing"

    def run(self, ctx: AgentContext) -> None:
        published: list[PublishedArticle] = ctx.state.get("published", [])
        ctx.state["marketing_actions"] = [
            f"Newsletter-Teaser für '{article.title}' erstellt" for article in published[:5]
        ]


class SocialMediaManagerAgent:
    name = "KI Agent 8"
    specialty = "Social Media"

    def run(self, ctx: AgentContext) -> None:
        published: list[PublishedArticle] = ctx.state.get("published", [])
        ctx.state["social_posts"] = [
            f"Post veröffentlicht: {article.title} #Nachrichten #Analyse" for article in published[:10]
        ]


class CEOAgent:
    name = "KI Agent 9"
    specialty = "Oversight"

    def run(self, ctx: AgentContext) -> None:
        count = len(ctx.state.get("published", []))
        report = DailyReport(
            created_at=datetime.utcnow(),
            summary=f"Tagesabschluss: {count} Artikel veröffentlicht.",
            proposed_improvements=[
                "Mehr regionale Themen integrieren.",
                "A/B-Test für Überschriften starten.",
                "Compliance-Regelkatalog monatlich aktualisieren.",
            ],
        )
        ctx.state["report"] = report
