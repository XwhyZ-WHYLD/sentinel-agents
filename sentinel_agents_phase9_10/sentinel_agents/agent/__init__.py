"""Agent subpackage for Sentinel Agents Phases 9 & 10.

Exports the `AgentRuntime` class and helper to construct a default
runtime instance.  See `runtime.py` for details.
"""

from .runtime import AgentRuntime, load_default_runtime  # noqa: F401

__all__ = ["AgentRuntime", "load_default_runtime"]