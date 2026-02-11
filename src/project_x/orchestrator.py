from __future__ import annotations

import threading
import time
from dataclasses import dataclass

from .agents.base import Agent, AgentContext
from .agents.team import (
    BackendDeveloperAgent,
    CEOAgent,
    FrontendDeveloperAgent,
    MarketingManagerAgent,
    PublisherAgent,
    QualityManagerAgent,
    ResearchSpecialistAgent,
    SocialMediaManagerAgent,
    TextWriterAgent,
)
from .config import Settings
from .repository import Repository


@dataclass
class AgentRegistry:
    agents: list[Agent]

    @classmethod
    def default(cls) -> "AgentRegistry":
        return cls(
            agents=[
                FrontendDeveloperAgent(),
                BackendDeveloperAgent(),
                ResearchSpecialistAgent(),
                TextWriterAgent(),
                QualityManagerAgent(),
                PublisherAgent(),
                MarketingManagerAgent(),
                SocialMediaManagerAgent(),
                CEOAgent(),
            ]
        )

    def add(self, agent: Agent) -> None:
        self.agents.append(agent)


class AutonomousNewsroom:
    def __init__(self, settings: Settings, repository: Repository, registry: AgentRegistry | None = None) -> None:
        self.settings = settings
        self.repository = repository
        self.registry = registry or AgentRegistry.default()
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    def run_cycle(self) -> dict:
        ctx = AgentContext(state={})
        for agent in self.registry.agents:
            agent.run(ctx)

        published = ctx.state.get("published", [])[: self.settings.min_articles_per_day]
        for article in published:
            self.repository.save_article(article)

        report = ctx.state.get("report")
        if report:
            self.repository.save_daily_report(report)
        return ctx.state

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        def worker() -> None:
            while not self._stop.is_set():
                self.run_cycle()
                self._stop.wait(self.settings.cycle_interval_seconds)

        self._thread = threading.Thread(target=worker, name="autonomous-newsroom", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)
