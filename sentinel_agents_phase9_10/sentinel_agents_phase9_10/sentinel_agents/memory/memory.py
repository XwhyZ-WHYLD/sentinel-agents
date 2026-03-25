"""JSON‑backed memory store for execution traces (Phases 9 & 10).

This simple implementation persists a list of traces to a JSON file on
disk.  Each trace is assigned a monotonically increasing identifier.
It is unchanged from earlier phases.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


class MemoryStore:
    """Persistent store for execution traces."""

    def __init__(self, path: str) -> None:
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)
        self._load()
        self._next_id = len(self._traces)

    def _load(self) -> None:
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                self._traces: List[Dict[str, Any]] = json.load(f)
            except json.JSONDecodeError:
                self._traces = []

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._traces, f, indent=2)

    def save_trace(self, trace: Dict[str, Any]) -> None:
        """Persist a trace and assign it a unique identifier."""
        trace = dict(trace)
        trace["id"] = self._next_id
        self._next_id += 1
        self._traces.append(trace)
        self._save()

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Return a list of traces containing the query substring in the task."""
        query_lower = query.lower()
        return [t for t in self._traces if query_lower in t.get("task", "").lower()][:max_results]

    def get_trace(self, trace_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a trace by its identifier."""
        for t in self._traces:
            if t.get("id") == trace_id:
                return t
        return None

    def __repr__(self) -> str:
        return f"MemoryStore(path={self.path}, traces={len(self._traces)})"