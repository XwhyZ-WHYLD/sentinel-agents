"""Governance engine for Sentinel Agents Phases 9 & 10.

This class encapsulates governance‑related actions.  Currently it
delegates to an `AuditLogger` to record each execution trace.  The
implementation is unchanged from Phase 8 but provides a place to
extend governance logic (e.g. compliance hooks, trace validation,
policy explainability) in the future.
"""

from __future__ import annotations

from typing import Any, Dict

from .audit_logger import AuditLogger


class GovernanceEngine:
    """Record execution traces for auditing and governance."""

    def __init__(self, audit_logger: AuditLogger) -> None:
        self.audit_logger = audit_logger

    def record(self, trace: Dict[str, Any]) -> None:
        """Record a trace through the audit logger."""
        self.audit_logger.log(trace)