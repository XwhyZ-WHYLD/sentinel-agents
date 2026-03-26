"""Adaptive learning engine for Sentinel Agents Phases 9 & 10.

Unchanged from earlier phases, this engine processes execution traces
by adjusting memory weights and feeding back risky output into the
policy engine.  More sophisticated learning algorithms can be
introduced here.
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
        self.adaptation = Adaptation(memory_store)
        self.feedback_loop = FeedbackLoop(policy_engine, risky_feedback_keywords or [])

    def process(self, trace: Dict[str, Any]) -> None:
        risk = trace.get("risk", 0)
        try:
            risk_value = float(risk)
        except (TypeError, ValueError):
            risk_value = 0.0
        if risk_value > 0:
            trace_id = trace.get("id")
            if trace_id is not None:
                self.adaptation.promote_trace(trace_id, weight=1.0 + risk_value)

        result = trace.get("result", "") or ""
        self.feedback_loop.update_policy_from_output(result)