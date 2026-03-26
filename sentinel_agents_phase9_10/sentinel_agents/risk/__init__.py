"""Risk scoring layer for Sentinel Agents Phases 9 & 10.

Exports the `RiskEngine`, which assigns a risk score based on risky
keywords.  This implementation is unchanged from earlier phases.
"""

from .risk_engine import RiskEngine  # noqa: F401

__all__ = ["RiskEngine"]