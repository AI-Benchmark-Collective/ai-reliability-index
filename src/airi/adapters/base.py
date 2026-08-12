from __future__ import annotations

from typing import Protocol

from airi.models import AdapterResult, TaskContext


class AgentAdapter(Protocol):
    """Provider-neutral contract for one isolated task attempt."""

    name: str
    model: str

    def capabilities(self) -> dict[str, bool]: ...

    def run(self, context: TaskContext) -> AdapterResult: ...
