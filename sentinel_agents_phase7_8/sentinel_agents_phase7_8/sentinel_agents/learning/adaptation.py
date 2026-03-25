"""Adaptation algorithms for Sentinel Agents Phase 7 & 8.

The `Adaptation` class provides simple mechanisms for modifying how the
memory store is used.  In this reference implementation we support
adjusting a weight for each stored trace.  Higher weights may influence
search ranking or prioritisation by the agent.  A real system might use
embeddings, vector similarity or reinforcement learning.
"""

from __future__ import annotations

from typing import Dict

from ..memory.memory import MemoryStore


class Adaptation:
    """Adjust memory weighting for stored execution traces."""

    def __init__(self, memory_store: MemoryStore) -> None:
        self.memory_store = memory_store
        # In‑memory map of trace_id -> weight; not persisted to disk
        self.weights: Dict[int, float] = {}

    def promote_trace(self, trace_id: int, weight: float) -> None:
        """Increase the weight for a given trace.

        Parameters
        ----------
        trace_id : int
            The identifier of the trace returned by `MemoryStore.save_trace`.
        weight : float
            The amount to add to the current weight.  If the trace is not
            present in the weight map it will be added.
        """
        self.weights[trace_id] = self.weights.get(trace_id, 0.0) + weight

    def get_weight(self, trace_id: int) -> float:
        """Return the stored weight for a trace, or 0 if none exists."""
        return self.weights.get(trace_id, 0.0)