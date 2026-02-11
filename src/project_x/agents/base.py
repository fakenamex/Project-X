from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class AgentContext:
    state: dict[str, Any]


class Agent(Protocol):
    name: str
    specialty: str

    def run(self, ctx: AgentContext) -> None:
        ...
