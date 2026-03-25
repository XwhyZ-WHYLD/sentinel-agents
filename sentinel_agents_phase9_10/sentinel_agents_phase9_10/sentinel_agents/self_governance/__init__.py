"""Self‑governance layer for Sentinel Agents Phase 10.

Exports the `SelfGovernanceEngine`, which adjusts policy and risk
parameters based on observed behaviour.  This layer enables the
system to adapt its own constraints over time.  The implementation
here is deliberately simple and demonstrates the concept of
self‑adjustment.
"""

from .self_governance_engine import SelfGovernanceEngine  # noqa: F401

__all__ = ["SelfGovernanceEngine"]