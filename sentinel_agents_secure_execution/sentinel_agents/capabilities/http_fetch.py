"""HTTP fetch capability.

Allows the agent to perform a simple HTTP GET request to retrieve the
contents of a URL.  This implementation uses the ``requests`` library
and returns the status code and first 500 characters of the response
body.  It should only be used for demonstration purposes; in a real
application you would add URL allowlists and handle many more edge
cases.
"""

from __future__ import annotations

from typing import Any, Dict

import requests


def http_fetch(url: str) -> Any:
    """Fetch a URL via HTTP GET.

    Parameters
    ----------
    url: str
        The URL to fetch.  Must include http:// or https://.

    Returns
    -------
    dict
        A dictionary with keys ``status_code`` and ``body`` (truncated).
    """
    if not url:
        return {"error": "no url provided"}
    if not url.startswith("http://") and not url.startswith("https://"):
        return {"error": "invalid url scheme"}
    try:
        resp = requests.get(url, timeout=5)
        # Truncate body for safety.
        body = resp.text[:500]
        return {"status_code": resp.status_code, "body": body}
    except Exception as exc:
        return {"error": str(exc)}
