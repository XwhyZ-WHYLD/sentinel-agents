"""Sandbox subpackage.

Provides a placeholder `SandboxRouter` for routing execution to secure
environments such as Docker or WebAssembly.  The current implementation
returns the input unmodified and does not perform any actual isolation.  In a
production system the sandbox would ensure tasks execute within tightly
controlled boundaries.
"""

from .sandbox_router import SandboxRouter  # noqa: F401