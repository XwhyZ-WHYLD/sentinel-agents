"""Naive risk scoring engine for Sentinel Agents Phases 9 & 10.

Assigns a risk score between 0 and 1 based on the presence of risky
keywords.  Tasks containing configured risky keywords are assigned
higher scores.  Unchanged from earlier phases.
"""

from __future__ import annotations

from typing import Iterable, Set


class RiskEngine:
    """Very basic risk scoring based on keyword detection."""

    def __init__(
        self,
        risky_keywords: Iterable[str] | None = None,
        max_allowed_risk: float = 1.0,
    ) -> None:
        self.risky_keywords: Set[str] = set(risky_keywords or ["delete", "drop", "shutdown"])
        self.max_allowed_risk = max_allowed_risk

    def score(self, task: str) -> float:
        task_lower = task.lower()
        count = sum(1 for kw in self.risky_keywords if kw.lower() in task_lower)
        return min(1.0, count / (len(self.risky_keywords) or 1))

    def __repr__(self) -> str:
        return f"RiskEngine(risky_keywords={self.risky_keywords}, max_allowed_risk={self.max_allowed_risk})"