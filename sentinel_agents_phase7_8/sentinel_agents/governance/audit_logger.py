"""Simple audit logging for Sentinel Agents Phase 8.

The `AuditLogger` writes each execution trace to a log file in JSON
lines format.  Each log entry is a single line of JSON representing
the trace dictionary.  In a full system, this could be extended to
write to structured logging services, add timestamps or include
cryptographic attestations.
"""

from __future__ import annotations

import json
from typing import Any, Dict


class AuditLogger:
    """Append execution traces to a JSON lines file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def log(self, trace: Dict[str, Any]) -> None:
        """Append a trace dictionary to the log file as a JSON line."""
        # Avoid exceptions from failing to serialise non‑JSON types
        safe_trace = json.loads(json.dumps(trace))
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(safe_trace) + "\n")