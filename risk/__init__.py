"""Risk module for Sentinel Agents.

This package exposes the :func:`evaluate_risk` function, which assigns a
numeric risk score to each tool invocation based on its name and
arguments.  The risk score is a float between 0.0 (no risk) and 1.0
(high risk).  Higher scores should trigger more secure sandbox
environments and potentially stricter policy checks.

Phase 3 introduces the risk engine as a first‑class component of the
Sentinel runtime.  By quantifying the danger posed by each action, the
system can make more nuanced decisions about how to execute it and what
constraints to apply.
"""

from .risk_engine import evaluate_risk

__all__ = ["evaluate_risk"]