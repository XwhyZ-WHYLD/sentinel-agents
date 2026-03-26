"""Sandbox layer for Sentinel Agents Phases 9 & 10.

Exports the `SandboxRouter`, which is currently a placeholder.  It can
be extended to route execution to different sandboxes such as WASM or
containers.  Unchanged from earlier phases.
"""

from .sandbox_router import SandboxRouter  # noqa: F401

__all__ = ["SandboxRouter"]