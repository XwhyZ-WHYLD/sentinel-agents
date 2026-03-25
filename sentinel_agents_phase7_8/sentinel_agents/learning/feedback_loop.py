"""Feedback loop for Sentinel Agents Phase 7 & 8.

The `FeedbackLoop` watches execution outputs and extracts potentially
risky tokens.  If the output contains certain risky keywords, those
tokens are fed back into the policy engine to be blocked on future
runs.  This mechanism is extremely simple but demonstrates how a
feedback loop can encourage safer behaviour over time.
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
        """Scan the output for risky feedback keywords and block them.

        This method examines the lower‑cased output and if any configured
        risky keywords are present it calls `PolicyEngine.update_policy` to
        add them to the blocked keyword list.  By doing so the system can
        learn to avoid repeating dangerous actions or content.
        """
        output_lower = output.lower()
        blocked: List[str] = []
        for kw in self.risky_feedback_keywords:
            if kw in output_lower:
                blocked.append(kw)
        if blocked:
            self.policy_engine.update_policy(blocked)