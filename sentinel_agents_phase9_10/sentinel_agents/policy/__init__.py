"""Policy enforcement layer for Sentinel Agents Phases 9 & 10.

Exports the `PolicyEngine`, a keyword‑based permission model.  This
implementation is unchanged from earlier phases but may be adapted by
self‑governance to update its blocked keywords.
"""

from .policy_engine import PolicyEngine  # noqa: F401

__all__ = ["PolicyEngine"]