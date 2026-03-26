"""Evaluation engine for Sentinel Agents Phases 9 & 10.

This module defines the `EvaluationEngine` class, responsible for
computing simple metrics about individual execution traces.  It
computes a quality score and a pass/fail flag based on the risk of
the task and whether a result was produced.  This implementation is
identical to the Phase 7 version and can be extended with more
sophisticated evaluation logic.
"""

from __future__ import annotations

from typing import Any, Dict

from ..memory.memory import MemoryStore
from ..risk.risk_engine import RiskEngine


class EvaluationEngine:
    """Compute metrics for execution traces."""

    def __init__(self, memory_store: MemoryStore, risk_engine: RiskEngine) -> None:
        self.memory_store = memory_store
        self.risk_engine = risk_engine

    def evaluate(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Return evaluation metrics for the given trace.

        The quality score is computed as `1 − risk` (clipped to [0, 1])
        and the pass criterion is that the risk does not exceed the
        maximum allowed risk configured on the risk engine and the
        execution produced a result.

        Parameters
        ----------
        trace : Dict[str, Any]
            The execution trace produced by the runtime.  Must contain
            a `risk` field and optionally a `result` field.

        Returns
        -------
        Dict[str, Any]
            A dictionary with `score` and `passed` keys.
        """
        risk = float(trace.get("risk", 0.0))
        score = max(0.0, 1.0 - risk)
        passed = risk <= self.risk_engine.max_allowed_risk and bool(trace.get("result"))
        return {"score": score, "passed": passed}