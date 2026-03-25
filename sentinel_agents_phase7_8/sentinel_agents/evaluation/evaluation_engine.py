"""Evaluation engine for Sentinel Agents Phase 7.

This module defines the `EvaluationEngine` class, responsible for
computing simple metrics about individual execution traces.  The goal
of Phase 7 is to introduce a layer that can assess whether the system
behaved as expected and provide a quantitative signal that can be
tracked over time.  In this reference implementation we compute a
single quality score based on the risk of the task and whether the
result was successfully produced.
"""

from __future__ import annotations

from typing import Any, Dict

from ..memory.memory import MemoryStore
from ..risk.risk_engine import RiskEngine


class EvaluationEngine:
    """Compute metrics for execution traces.

    Parameters
    ----------
    memory_store : MemoryStore
        The persistent store from which traces can be retrieved.  While
        not used heavily in this simple implementation, the memory
        store provides context for more sophisticated evaluations.
    risk_engine : RiskEngine
        The risk engine used to compute the original risk scores.  The
        evaluation engine may reference risk thresholds to decide
        pass/fail outcomes.

    Notes
    -----
    A real evaluation layer might perform regression testing, compute
    confidence metrics or detect hallucinations.  This simple version
    produces only a score in [0, 1] where higher is better and a
    boolean `passed` indicator.
    """

    def __init__(self, memory_store: MemoryStore, risk_engine: RiskEngine) -> None:
        self.memory_store = memory_store
        self.risk_engine = risk_engine

    def evaluate(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Return evaluation metrics for the given trace.

        The quality score is computed as `1 − risk` (clipped to [0, 1])
        and the pass criterion is that the risk does not exceed the
        maximum allowed risk configured on the risk engine.

        Parameters
        ----------
        trace : Dict[str, Any]
            The execution trace produced by the runtime.  Must contain
            a `risk` field and optionally an `result` field.

        Returns
        -------
        Dict[str, Any]
            A dictionary with `score` and `passed` keys.
        """
        risk = float(trace.get("risk", 0.0))
        # Quality is higher for lower risk; ensure result exists
        score = max(0.0, 1.0 - risk)
        passed = risk <= self.risk_engine.max_allowed_risk and bool(trace.get("result"))
        return {"score": score, "passed": passed}