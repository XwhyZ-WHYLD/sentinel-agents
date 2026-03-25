"""Simple swarm coordinator for running multiple agents in sequence.

This module defines a `SwarmCoordinator` class that accepts a list of
`AgentRuntime` instances and dispatches a task to each in order.  Each
agent processes the task independently.  The results are collected and
returned.  In a more sophisticated implementation the coordinator could
distribute sub‑tasks, aggregate results and handle failure scenarios.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ..agent.runtime import AgentRuntime


class SwarmCoordinator:
    """Coordinate a list of agent runtimes to process tasks sequentially."""

    def __init__(self, agents: Iterable[AgentRuntime]) -> None:
        self.agents: List[AgentRuntime] = list(agents)

    def run(self, task: str) -> List[Dict[str, Any]]:
        """Execute the same task across all agents and collect their outputs."""
        outputs: List[Dict[str, Any]] = []
        for agent in self.agents:
            outputs.append(agent.execute_task(task))
        return outputs

    def __repr__(self) -> str:  # pragma: no cover
        return f"SwarmCoordinator(num_agents={len(self.agents)})"