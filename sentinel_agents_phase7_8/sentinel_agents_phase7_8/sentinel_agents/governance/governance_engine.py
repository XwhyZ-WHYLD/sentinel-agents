"""Governance engine for Sentinel Agents Phase 8.

This class encapsulates governance‑related actions for the runtime.  At
present it delegates all work to an `AuditLogger` but provides a
forward‑compatible place to implement traceability, policy
explainability and compliance logic.  The interface is intentionally
minimal: for each execution trace the governance layer is notified via
the `record` method.
"""

from __future__ import annotations

from typing import Any, Dict

from .audit_logger import AuditLogger


class GovernanceEngine:
    """Record execution traces for auditing and governance."""

    def __init__(self, audit_logger: AuditLogger) -> None:
        self.audit_logger = audit_logger

    def record(self, trace: Dict[str, Any]) -> None:
        """Record a trace through the audit logger.

        Parameters
        ----------
        trace : Dict[str, Any]
            The execution trace produced by the runtime.  It will be
            serialised and written to the log via the underlying
            `AuditLogger`.  Future governance logic could also
            validate the trace or enforce compliance constraints here.
        """
        self.audit_logger.log(trace)