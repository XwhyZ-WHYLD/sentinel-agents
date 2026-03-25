"""Risk scoring layer for Sentinel Agents Phase 7 & 8.

Exports the `RiskEngine` class used to assign a risk score to tasks.
This implementation is unchanged from Phase 6 and remains simple but
demonstrates where more sophisticated risk assessment could be added.
"""

from .risk_engine import RiskEngine  # noqa: F401

__all__ = ["RiskEngine"]