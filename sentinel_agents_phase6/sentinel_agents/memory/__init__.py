"""Memory subpackage.

Provides a simple file‑backed memory store used to persist and search
execution traces.  Phase 6 leverages this store for adaptive learning.
"""

from .memory import MemoryStore  # noqa: F401