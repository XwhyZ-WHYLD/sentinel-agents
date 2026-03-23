"""Basic policy engine for Sentinel Agents Phase 6.

The `PolicyEngine` provides a minimal permission model.  It holds a set of
blocked keywords and exposes `is_allowed` for checking tasks.  The learning
layer can adjust the blocked keywords via `update_policy`.
"""

from __future__ import annotations

from typing import Iterable, Set


class PolicyEngine:
    """Simple policy engine enforcing keyword‑based permissions."""

    def __init__(self, blocked_keywords: Iterable[str] | None = None) -> None:
        # A set of forbidden substrings.  If a task contains any of these
        # keywords, it will be denied.  Defaults to an empty set (allow all).
        self.blocked_keywords: Set[str] = set(blocked_keywords or [])

    def is_allowed(self, task: str) -> bool:
        """Return `True` if the task is permitted by the current policy."""
        task_lower = task.lower()
        return not any(kw.lower() in task_lower for kw in self.blocked_keywords)

    def update_policy(self, blocked_keywords: Iterable[str]) -> None:
        """Update the set of blocked keywords.

        The learning layer can call this method to introduce new
        restrictions based on feedback from previous executions.  The
        update is additive—existing blocked keywords will persist.
        """
        for kw in blocked_keywords:
            self.blocked_keywords.add(kw)

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"PolicyEngine(blocked_keywords={self.blocked_keywords})"