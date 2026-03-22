"""Memory subsystem for Sentinel Agents.

This package provides a simple persistent memory system that allows
agents to record episodic events (such as tool invocations, policy
decisions and conversation turns) and query them later.  The memory
subsystem was introduced in Phase 5 of the Sentinel project to give
agents a basic form of persistence between runs.

The default implementation writes all memory entries to a JSON file
on disk.  Each entry is stored with a timestamp, an event type and
arbitrary event data.  Users can customise the storage location by
passing a different path when constructing the MemoryManager.

The API of the memory subsystem is intentionally small.  See
``sentinel_agents/memory/memory.py`` for implementation details.
"""

from .memory import MemoryManager  # noqa: F401