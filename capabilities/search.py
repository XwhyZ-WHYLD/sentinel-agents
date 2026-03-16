"""Search capability.

This is a stub implementation of a search tool.  In a real
application you would call an API such as Bing or Google Custom Search
and return structured results.  To keep the MVP dependency‑free and
network agnostic, we simply echo back the query.
"""

from __future__ import annotations

from typing import Any


def search(query: str) -> Any:
    """Perform a search.

    Parameters
    ----------
    query: str
        The search query.

    Returns
    -------
    dict
        A simple dictionary containing the query string and a note that
        this is a stub.  Replace this implementation with a real
        search API if desired.
    """
    return {
        "type": "search_result",
        "query": query,
        "results": [
            {
                "title": f"Search result for '{query}'",
                "snippet": "This search tool is a stub and does not call any external API.",
            }
        ],
    }
