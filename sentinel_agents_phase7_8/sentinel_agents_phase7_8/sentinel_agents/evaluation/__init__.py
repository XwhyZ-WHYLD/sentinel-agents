"""Evaluation layer for Sentinel Agents Phase 7.

This subpackage contains simple facilities for evaluating the behaviour
of the agent runtime.  The primary component is the `EvaluationEngine`,
which computes a basic quality score from an execution trace and
determines whether the execution passed minimal criteria.  Additional
modules (such as regression suites, scenarios and metrics definitions)
can be added here as the system evolves.
"""

from .evaluation_engine import EvaluationEngine  # noqa: F401

__all__ = ["EvaluationEngine"]