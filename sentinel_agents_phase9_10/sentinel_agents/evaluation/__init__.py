"""Evaluation layer for Sentinel Agents Phases 9 & 10.

Exports the `EvaluationEngine`, which computes simple quality metrics
for execution traces.  The implementation is identical to the Phase 7
version and serves as a scaffold for more advanced evaluation logic.
"""

from .evaluation_engine import EvaluationEngine  # noqa: F401

__all__ = ["EvaluationEngine"]