"""Naive risk scoring engine (Phase 7 & 8).

The `RiskEngine` assigns a risk score between 0 and 1.  Tasks
containing configured risky keywords are assigned higher scores.  A
maximum allowed risk threshold can be specified when constructing the
engine.  This implementation mirrors the Phase 6 version and
illustrates how risk evaluation fits into the runtime.
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
        # Upper bound for risk; tasks scoring above this are denied.
        self.max_allowed_risk = max_allowed_risk

    def score(self, task: str) -> float:
        """Return a risk score between 0 and 1 for the given task."""
        task_lower = task.lower()
        # Count risky keyword occurrences and normalise by number of keywords.
        count = sum(1 for kw in self.risky_keywords if kw.lower() in task_lower)
        return min(1.0, count / (len(self.risky_keywords) or 1))

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"RiskEngine(risky_keywords={self.risky_keywords}, max_allowed_risk={self.max_allowed_risk})"