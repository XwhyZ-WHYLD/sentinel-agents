"""Simple policy engine for Sentinel Agents.

The policy engine is responsible for approving or denying tool calls
based on the agent’s identity, the capability being requested and the
arguments provided.  In this MVP implementation the policy is very
basic:

* If the capability name is not in the agent’s allowed permissions,
  the call is denied.
* ``read_file`` and ``write_file`` are allowed only on paths that do not
  contain ``..`` (to prevent escaping the workspace).
* ``http_fetch`` is allowed only on ``https://`` URLs (no plain http).

You can extend this class with more sophisticated rules or load
policies from configuration.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


class PolicyEngine:
    """A policy engine that approves or denies tool calls."""

    def __init__(self, permissions: List[str]) -> None:
        self.permissions = permissions

    def check(self, agent_name: str, tool_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """Return whether the call is allowed and a human readable reason.

        Parameters
        ----------
        agent_name: str
            Name of the agent.
        tool_name: str
            Name of the capability being requested.
        args: dict
            Arguments for the capability.

        Returns
        -------
        (allowed, reason)
            ``allowed`` is ``True`` if the call is permitted.  ``reason``
            explains why the call was allowed or denied.
        """
        # Deny if tool is not permitted.
        if tool_name not in self.permissions:
            return False, f"{agent_name} does not have permission for {tool_name}"

        # Additional checks based on the capability.
        if tool_name in {"read_file", "write_file"}:
            path = args.get("path") or args.get("file")
            if path is not None and ".." in path:
                return False, "path traversal is not allowed"
        if tool_name == "http_fetch":
            url = args.get("url")
            if url and not url.startswith("https://"):
                return False, "only HTTPS fetches are allowed"
        # If none of the rules deny the call, allow it.
        return True, "allowed"
