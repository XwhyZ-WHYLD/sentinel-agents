"""Sandbox layer for Sentinel Agents Phase 7 & 8.

Exports the `SandboxRouter`, which dispatches capability execution to
different sandboxes (e.g. WASM, container, Firecracker).  In this
reference implementation we provide only a placeholder router and do
not execute any untrusted code.  See `sandbox_router.py` for details.
"""

from .sandbox_router import SandboxRouter  # noqa: F401

__all__ = ["SandboxRouter"]