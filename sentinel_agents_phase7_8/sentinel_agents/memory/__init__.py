"""Memory layer for Sentinel Agents Phase 7 & 8.

This package exposes a simple JSON‑backed `MemoryStore` used to
persist execution traces.  It mirrors the Phase 6 implementation and
serves as a basic persistence mechanism for the runtime.
"""

from .memory import MemoryStore  # noqa: F401

__all__ = ["MemoryStore"]