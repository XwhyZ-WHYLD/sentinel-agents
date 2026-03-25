"""Adaptive learning engine for Sentinel Agents Phase 7 & 8.

The `LearningEngine` orchestrates adaptive behaviour in the system.  It
observes execution traces, updates memory weighting and uses feedback to
adjust the policy.  This reference implementation is intentionally
lightweight—it demonstrates how to plug a learning layer into the
Sentinel Agents architecture without prescribing a specific algorithm.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from ..memory.memory import MemoryStore
from ..policy.policy_engine import PolicyEngine
from .feedback_loop import FeedbackLoop
from .adaptation import Adaptation


class LearningEngine:
    """Coordinate learning operations based on execution traces."""

    def __init__(
        self,
        memory_store: MemoryStore,
        policy_engine: PolicyEngine,
        risky_feedback_keywords: Optional[Iterable[str]] = None,
    ) -> None:
        self.memory_store = memory_store
        self.policy_engine = policy_engine
        # Components for adaptation and feedback
        self.adaptation = Adaptation(memory_store)
        self.feedback_loop = FeedbackLoop(policy_engine, risky_feedback_keywords or [])

    def process(self, trace: Dict[str, Any]) -> None:
        """Process an execution trace for learning.

        This method performs two primary actions:

        * Adjust memory weights or indices based on the contents of the trace.
        * Feed back any risky outputs into the policy engine.

        The reference implementation uses very simple heuristics.  In
        production you might implement RL or statistical methods here.
        """
        # Adapt memory: for now we simply flag traces with non‑zero risk for priority.
        risk = trace.get("risk", 0)
        try:
            risk_value = float(risk)
        except (TypeError, ValueError):
            risk_value = 0.0
        if risk_value > 0:
            # Promote the trace if an identifier is available.  The
            # MemoryStore assigns the ID when saving but does not
            # mutate the passed dictionary, so guard against missing IDs.
            trace_id = trace.get("id")
            if trace_id is not None:
                self.adaptation.promote_trace(int(trace_id), weight=1.0 + risk_value)

        # Feedback: update policy based on risky keywords found in the result
        result = trace.get("result", "") or ""
        self.feedback_loop.update_policy_from_output(result)