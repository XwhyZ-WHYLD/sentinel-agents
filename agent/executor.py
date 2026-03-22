"""Executor dispatches tool calls to their implementations.

This module defines :func:`execute` which takes a capability name and
arguments, then calls the corresponding function from the
``sentinel_agents.capabilities`` package.  If a capability is not
implemented it raises ``NotImplementedError``.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple, Callable

# Phase 3 imports for risk evaluation and sandbox execution
from ..policy.policy_engine import PolicyEngine
from ..risk import evaluate_risk
from ..sandbox.router import choose_sandbox, execute_in_sandbox, SandboxType


def execute(tool_name: str, args: Dict[str, Any]) -> Any:
    """Execute a capability by name.

    Parameters
    ----------
    tool_name: str
        Name of the capability to execute.
    args: dict
        Keyword arguments for the capability.

    Returns
    -------
    Any
        Result returned by the capability implementation.

    Raises
    ------
    NotImplementedError
        If the capability is unknown.
    """
    if tool_name == "search":
        from ..capabilities import search as search_cap
        return search_cap.search(args.get("query", ""))
    if tool_name == "http_fetch":
        from ..capabilities import http_fetch as http_cap
        return http_cap.http_fetch(args.get("url"))
    if tool_name == "read_file":
        from ..capabilities import filesystem as fs_cap
        return fs_cap.read_file(args.get("path"))
    if tool_name == "write_file":
        from ..capabilities import filesystem as fs_cap
        return fs_cap.write_file(args.get("path"), args.get("content", ""))
    raise NotImplementedError(f"Unknown capability: {tool_name}")


# ---------------------------------------------------------------------------
# Phase 3: risk‑aware execution

def _lookup_capability(tool_name: str) -> Callable[..., Any]:
    """Resolve a capability name to its implementation function.

    Parameters
    ----------
    tool_name: str
        Name of the capability.

    Returns
    -------
    Callable[..., Any]
        The function implementing the capability.

    Raises
    ------
    NotImplementedError
        If the capability is unknown.
    """
    if tool_name == "search":
        from ..capabilities import search as search_cap
        return lambda *a, **kw: search_cap.search(*a, **kw)
    if tool_name == "http_fetch":
        from ..capabilities import http_fetch as http_cap
        return lambda *a, **kw: http_cap.http_fetch(*a, **kw)
    if tool_name == "read_file":
        from ..capabilities import filesystem as fs_cap
        return lambda *a, **kw: fs_cap.read_file(*a, **kw)
    if tool_name == "write_file":
        from ..capabilities import filesystem as fs_cap
        return lambda *a, **kw: fs_cap.write_file(*a, **kw)
    raise NotImplementedError(f"Unknown capability: {tool_name}")


def execute_with_policy(
    agent_name: str,
    tool_name: str,
    args: Dict[str, Any],
    policy: PolicyEngine,
) -> Tuple[Any, Dict[str, Any]]:
    """Execute a capability within the risk/policy framework.

    This helper combines risk evaluation, policy checking, sandbox selection
    and audit logging.  It computes a risk score for the requested
    capability, consults the policy engine to approve or deny the call,
    chooses an appropriate sandbox based on the risk, and finally runs
    the capability function in that sandbox.

    Parameters
    ----------
    agent_name: str
        Name of the agent making the request.
    tool_name: str
        Name of the capability being invoked.
    args: dict
        Arguments for the capability.
    policy: PolicyEngine
        Policy engine used to validate the call.

    Returns
    -------
    (result, log_entry)
        ``result`` is the return value of the capability function or
        ``None`` if the call was denied.  ``log_entry`` is a dict
        recording the tool call, arguments, risk score, sandbox type,
        policy decision and result.
    """
    # Compute a risk score for the call.
    risk_score = evaluate_risk(tool_name, args)
    allowed, reason = policy.check(agent_name, tool_name, args)
    log_entry: Dict[str, Any] = {
        "tool": tool_name,
        "args": args,
        "risk_score": risk_score,
        "allowed": allowed,
        "reason": reason,
    }
    if not allowed:
        # Denied calls are not executed.
        log_entry["sandbox"] = None
        log_entry["result"] = None
        return None, log_entry
    # Determine the capability function.
    try:
        capability_func = _lookup_capability(tool_name)
    except NotImplementedError as exc:
        log_entry["sandbox"] = None
        log_entry["result"] = None
        log_entry["allowed"] = False
        log_entry["reason"] = str(exc)
        return None, log_entry
    # Select the sandbox based on risk.
    sandbox = choose_sandbox(tool_name, risk_score=risk_score)
    log_entry["sandbox"] = sandbox.name.lower()
    # Execute the capability in the chosen sandbox.
    result = execute_in_sandbox(sandbox, capability_func, **args)
    log_entry["result"] = result
    return result, log_entry
