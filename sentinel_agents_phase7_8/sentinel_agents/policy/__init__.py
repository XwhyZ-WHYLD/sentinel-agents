"""Policy enforcement layer for Sentinel Agents Phase 7 & 8.

Exports the `PolicyEngine`, a simple keyword‑based permission model used
to decide whether tasks are allowed.  The learning and governance
layers can update the set of blocked keywords over time.
"""

from .policy_engine import PolicyEngine  # noqa: F401

__all__ = ["PolicyEngine"]