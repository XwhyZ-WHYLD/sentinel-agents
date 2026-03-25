"""Adaptation algorithms for Sentinel Agents Phases 9 & 10.

This class is identical to earlier phases and provides a simple
mechanism for adjusting weights on stored traces.  It can be used
by the learning engine to prioritise certain memories.
"""

from __future__ import annotations

from typing import Dict

from ..memory.memory import MemoryStore


class Adaptation:
    """Adjust memory weighting for stored execution traces."""

    def __init__(self, memory_store: MemoryStore) -> None:
        self.memory_store = memory_store
        self.weights: Dict[int, float] = {}

    def promote_trace(self, trace_id: int, weight: float) -> None:
        self.weights[trace_id] = self.weights.get(trace_id, 0.0) + weight

    def get_weight(self, trace_id: int) -> float:
        return self.weights.get(trace_id, 0.0)