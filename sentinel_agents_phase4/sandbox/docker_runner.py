"""Sandbox runner.

In a real system this module would use a container runtime such as
Docker or Firecracker to execute agent actions in isolation.  For
simplicity the MVP does not implement actual sandboxing.  The
``run_in_sandbox`` function simply calls the provided function
directly.  You can extend this file to integrate containerized
execution.
"""

from __future__ import annotations

from typing import Any, Callable


def run_in_sandbox(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Execute a callable within a sandbox.

    This stub implementation just calls the function directly.  In a real
    system you would spin up a Docker container, copy the necessary
    files into it, run the function inside the container and then
    collect the result.
    """
    return func(*args, **kwargs)
