"""Feedback loop for Sentinel Agents Phases 9 & 10.

This class is unchanged from earlier phases.  It extracts risky
keywords from execution outputs and updates the policy accordingly.
"""

from __future__ import annotations

from typing import Iterable, List

from ..policy.policy_engine import PolicyEngine


class FeedbackLoop:
    """Extract risky keywords from execution outputs and update policy."""

    def __init__(self, policy_engine: PolicyEngine, risky_feedback_keywords: Iterable[str]) -> None:
        self.policy_engine = policy_engine
        self.risky_feedback_keywords: List[str] = [kw.lower() for kw in risky_feedback_keywords]

    def update_policy_from_output(self, output: str) -> None:
        output_lower = output.lower()
        blocked: List[str] = []
        for kw in self.risky_feedback_keywords:
            if kw in output_lower:
                blocked.append(kw)
        if blocked:
            self.policy_engine.update_policy(blocked)