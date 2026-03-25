"""Simple audit logging for Sentinel Agents Phases 9 & 10.

The `AuditLogger` writes each execution trace to a log file in JSON
lines format.  Each log entry is a single line of JSON representing
the trace dictionary.  This implementation is unchanged from Phase 8.
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
        safe_trace = json.loads(json.dumps(trace))
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(safe_trace) + "\n")