"""Sandbox router for sentinel_agents.

This module selects an appropriate sandbox backend (WASM, Firecracker, or Docker)
for executing capability functions based on the tool name or a simple risk
heuristic.  It then dispatches execution to the corresponding sandbox runner.

This router is a critical component of Phase 2 (Secure Execution Layer).  It
allows the system to run trusted and untrusted code in appropriate isolation
contexts.  At the moment, the implementation is minimal and delegates to
placeholder sandbox runners.  In a real deployment, the WASM runner would
compile and execute WebAssembly modules using ``wasmtime`` or a similar
runtime, the Firecracker runner would spin up microVMs for untrusted code, and
the Docker runner would handle heavier workloads.
"""

from enum import Enum, auto
from typing import Callable, Any, Optional

from . import docker_runner
try:
    from . import wasm_runner
except ImportError:
    wasm_runner = None  # type: ignore
try:
    from . import firecracker_runner
except ImportError:
    firecracker_runner = None  # type: ignore


class SandboxType(Enum):
    """Enumeration of available sandbox backends."""
    WASM = auto()
    FIRECRACKER = auto()
    DOCKER = auto()


def choose_sandbox(tool_name: str, risk_score: Optional[float] = None) -> SandboxType:
    """Select a sandbox backend based on the capability/tool name.

    Parameters
    ----------
    tool_name: str
        The name of the capability requested.

    Returns
    -------
    SandboxType
        The chosen sandbox backend.

    Notes
    -----
    This function implements a simple heuristic: file system access and other
    potentially sensitive operations are routed to the more secure Firecracker
    backend, whereas lightweight operations (e.g. search or HTTP fetch) go
    through the WASM backend for speed.  All other operations fall back to
    Docker.  In the future, this could be extended with policy-based or
    risk-scoring routing.
    """
    # When a risk score is provided, use it to determine the sandbox.
    # Risk < 0.3 -> WASM (fast path)
    # 0.3 ≤ risk < 0.7 -> Docker (moderate isolation)
    # ≥ 0.7 -> Firecracker (secure path)
    if risk_score is not None:
        if risk_score < 0.3:
            return SandboxType.WASM
        if risk_score < 0.7:
            return SandboxType.DOCKER
        return SandboxType.FIRECRACKER
    # Fallback to heuristics based on tool name.
    high_risk = {"read_file", "write_file"}
    if tool_name in high_risk:
        return SandboxType.FIRECRACKER
    low_risk = {"search", "http_fetch"}
    if tool_name in low_risk:
        return SandboxType.WASM
    return SandboxType.DOCKER


def execute_in_sandbox(sandbox: SandboxType, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Execute a function within the selected sandbox.

    Parameters
    ----------
    sandbox: SandboxType
        The sandbox backend to use.
    func: callable
        The capability function to execute.
    args: tuple
        Positional arguments for the capability function.
    kwargs: dict
        Keyword arguments for the capability function.

    Returns
    -------
    Any
        The result of executing the capability function.

    Notes
    -----
    The current implementation simply calls the sandbox runner's
    ``run_in_sandbox`` function, which in this MVP returns the result of the
    function directly.  In a production system, these calls would manage the
    lifecycle of a sandboxed environment and enforce resource limits and
    isolation.
    """
    if sandbox == SandboxType.WASM and wasm_runner is not None:
        return wasm_runner.run_in_sandbox(func, *args, **kwargs)
    if sandbox == SandboxType.FIRECRACKER and firecracker_runner is not None:
        return firecracker_runner.run_in_sandbox(func, *args, **kwargs)
    # Fallback to Docker for any unknown or unsupported sandbox
    return docker_runner.run_in_sandbox(func, *args, **kwargs)
