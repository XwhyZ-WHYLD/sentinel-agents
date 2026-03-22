"""Persistent memory subsystem for Sentinel Agents.

The MemoryManager class implements a simple JSON‑backed store for
agent memories.  Each memory entry consists of a timestamp, an
``event_type`` string and an arbitrary ``event_data`` payload.  When
constructed, the MemoryManager will load any existing memory file on
disk.  All modifications are immediately written back to disk to
ensure durability.

This design trades sophistication for simplicity: it does not
implement vector search or embedding‑based retrieval.  Instead, it
performs a very simple substring search over the ``event_type`` and
``event_data`` fields.  For small projects this is sufficient and
avoids extra dependencies.  More sophisticated implementations could
replace this with a vector database or other backend while retaining
the same API.
"""

from __future__ import annotations

import json
import os
import threading
import time
from typing import Any, Dict, List, Optional


class MemoryManager:
    """Manage persistent memory entries for agents.

    Parameters
    ----------
    memory_path: str
        Path to the JSON file on disk where memories should be stored.
        The default location is ``~/.sentinel_agents/memory.json``.  If
        the file or its parent directories do not exist they will be
        created automatically.
    """

    def __init__(self, memory_path: Optional[str] = None) -> None:
        if memory_path is None:
            home = os.path.expanduser("~")
            memory_path = os.path.join(home, ".sentinel_agents", "memory.json")
        self.memory_path = memory_path
        self._lock = threading.Lock()
        self._entries: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        """Load existing memory entries from disk, if present."""
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    self._entries = json.load(f)
            else:
                self._entries = []
        except Exception:
            # If the file is corrupted or unreadable, reset it.  This is
            # defensive coding: in production you might want to log a
            # warning or attempt to recover.
            self._entries = []

    def _save(self) -> None:
        """Persist current memory entries to disk."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self._entries, f, indent=2)

    def record_event(self, event_type: str, event_data: Any) -> None:
        """Record a new event in memory.

        This method is thread‑safe.  It appends a new entry to the
        internal list and writes the full list back to disk.  ``event_data``
        should be serialisable to JSON.  Complex objects will be
        converted to strings using ``repr``.

        Parameters
        ----------
        event_type: str
            A short identifier for the type of event being recorded
            (e.g. ``"tool_call"``, ``"user_input"``, ``"agent_response"``).
        event_data: Any
            Arbitrary data associated with the event.  Must be JSON
            serialisable, or convertible to a string.
        """
        entry = {
            "timestamp": time.time(),
            "event_type": str(event_type),
            "event_data": event_data,
        }
        with self._lock:
            self._entries.append(entry)
            try:
                # Try to serialise event_data to ensure JSON compliance
                json.dumps(entry, ensure_ascii=False)
            except Exception:
                entry["event_data"] = repr(event_data)
            self._save()

    def query(self, keyword: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Return memory entries matching a keyword.

        If ``keyword`` is None, all entries are returned.  Otherwise a
        case‑insensitive substring search is performed against the
        JSON‑serialised representation of each entry.  The results are
        ordered chronologically.

        Parameters
        ----------
        keyword: str, optional
            Substring to search for in the memory entries.  If omitted,
            all entries are returned.
        limit: int, optional
            Maximum number of entries to return.  If omitted, no limit
            is applied.

        Returns
        -------
        list of dict
            A list of memory entry dictionaries in the order they were
            recorded (oldest first).
        """
        with self._lock:
            if keyword is None:
                entries = list(self._entries)
            else:
                keyword_lower = keyword.lower()
                entries = [
                    e
                    for e in self._entries
                    if keyword_lower in json.dumps(e, ensure_ascii=False).lower()
                ]
            if limit is not None:
                entries = entries[-limit:]
            return entries

    def clear(self) -> None:
        """Erase all memory entries permanently and save an empty file."""
        with self._lock:
            self._entries = []
            self._save()