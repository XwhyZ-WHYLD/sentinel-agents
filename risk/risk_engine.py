"""Risk engine for Sentinel Agents.

The risk engine provides a simple heuristic to score the potential
danger of executing a given capability with specific arguments.  It
returns a float between 0.0 and 1.0, where higher values indicate a
greater likelihood of causing harm or requiring strong isolation.

This initial implementation is deliberately conservative and can be
extended or replaced with more sophisticated models.  The heuristics
below capture a few intuitive notions:

* File system operations are relatively high risk because they can
  expose sensitive data or write malicious files.
* Network fetches carry moderate risk; non‑HTTPS URLs are penalised.
* Simple search queries are low risk.
* Unknown tools default to medium risk.
"""

from __future__ import annotations

from typing import Any, Dict
import re


def evaluate_risk(tool_name: str, args: Dict[str, Any]) -> float:
    """Compute a risk score for a tool invocation.

    Parameters
    ----------
    tool_name: str
        Name of the capability being invoked.
    args: Dict[str, Any]
        Arguments provided to the capability.

    Returns
    -------
    float
        A risk score between 0.0 (no risk) and 1.0 (maximum risk).

    Notes
    -----
    This function uses heuristics rather than hard guarantees.  It is
    intended as a starting point and should be tuned based on real‑world
    experience.  Future versions may incorporate static analysis of
    code, user reputation, or machine‑learned models.
    """
    tool = tool_name.lower()
    # Base risk for known tools.
    if tool in {"read_file", "write_file"}:
        # File operations are high risk by default.
        risk = 0.7
        path = args.get("path") or args.get("file")
        if isinstance(path, str):
            # Penalise parent directory traversal.
            if ".." in path:
                risk += 0.2
            # Slightly lower risk for obvious non‑sensitive files
            if re.match(r"^/?tmp/", path):
                risk -= 0.1
        return min(max(risk, 0.0), 1.0)
    if tool == "http_fetch":
        risk = 0.5
        url = args.get("url") or ""
        # Penalise non‑HTTPS schemes.
        if isinstance(url, str) and not url.startswith("https://"):
            risk += 0.2
        # Low risk for localhost or internal API endpoints.
        if re.match(r"^https://(localhost|127\\.0\\.0\\.1)", url):
            risk -= 0.2
        return min(max(risk, 0.0), 1.0)
    if tool == "search":
        # Searching is relatively harmless.
        return 0.2
    # Unknown capabilities default to a medium risk.
    return 0.5