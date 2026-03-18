"""Executor dispatches tool calls to their implementations.

This module defines :func:`execute` which takes a capability name and
arguments, then calls the corresponding function from the
``sentinel_agents.capabilities`` package.  If a capability is not
implemented it raises ``NotImplementedError``.
"""

from __future__ import annotations

from typing import Any, Dict


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
