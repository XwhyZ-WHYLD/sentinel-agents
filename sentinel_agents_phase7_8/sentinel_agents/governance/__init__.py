"""Governance and audit layer for Sentinel Agents Phase 8.

This subpackage provides simple facilities for recording execution
traces to an audit log.  The primary components are the `AuditLogger`,
which writes traces to a JSON lines file, and the `GovernanceEngine`,
which orchestrates logging and any future governance logic.  These
classes form the foundation for more advanced features such as
traceability, policy explainability and compliance hooks.
"""

from .audit_logger import AuditLogger  # noqa: F401
from .governance_engine import GovernanceEngine  # noqa: F401

__all__ = ["AuditLogger", "GovernanceEngine"]