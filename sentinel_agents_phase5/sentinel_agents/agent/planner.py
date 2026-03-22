"""Simple planner for deciding which capability to call.

In a fully fledged agent you might use a large language model (LLM)
to decide on tools and arguments.  For this MVP we instead use a
very basic keyword heuristic.  It looks for certain verbs in the
user’s prompt and maps them to available capabilities if the agent
has been granted the necessary permission.
"""

from __future__ import annotations

from typing import List, Tuple, Optional, Dict, Any


def decide_tool(prompt: str, permissions: List[str]) -> Tuple[Optional[str], Dict[str, Any]]:
    """Return the name of the capability to call and its arguments.

    Parameters
    ----------
    prompt: str
        User’s natural language request.
    permissions: List[str]
        Capability names the agent is allowed to call.

    Returns
    -------
    (tool_name, args)
        ``tool_name`` is ``None`` if no tool should be called.  ``args``
        is a dictionary of arguments to pass to the executor.
    """
    lower_prompt = prompt.lower()
    # If the prompt asks to find or search something and we have the
    # permission, call the search capability.
    if any(keyword in lower_prompt for keyword in ["find", "search", "look up"]):
        if "search" in permissions:
            return "search", {"query": prompt}
    # If the prompt mentions fetching a URL.
    if "http" in lower_prompt or "https" in lower_prompt:
        if "http_fetch" in permissions:
            # Extract URL (rudimentary).
            words = prompt.split()
            url = next((w for w in words if w.startswith("http")), None)
            return "http_fetch", {"url": url}
    # Otherwise, nothing to do.
    return None, {}
