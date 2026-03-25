"""Basic policy engine for Sentinel Agents Phases 9 & 10.

This module implements a minimal permission model.  It holds a set of
blocked keywords and exposes `is_allowed` for checking tasks.  The
self‑governance engine can call `update_policy` to introduce new
restrictions.  Unchanged from earlier phases.
"""

from __future__ import annotations

from typing import Iterable, Set


class PolicyEngine:
    """Simple policy engine enforcing keyword‑based permissions."""

    def __init__(self, blocked_keywords: Iterable[str] | None = None) -> None:
        self.blocked_keywords: Set[str] = set(blocked_keywords or [])

    def is_allowed(self, task: str) -> bool:
        task_lower = task.lower()
        return not any(kw.lower() in task_lower for kw in self.blocked_keywords)

    def update_policy(self, blocked_keywords: Iterable[str]) -> None:
        for kw in blocked_keywords:
            self.blocked_keywords.add(kw)

    def __repr__(self) -> str:
        return f"PolicyEngine(blocked_keywords={self.blocked_keywords})"