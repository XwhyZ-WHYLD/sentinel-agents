"""API subpackage.

This package exposes a simple FastAPI endpoint for executing tasks via the
`AgentRuntime`.  It demonstrates how an external caller could interact
with the Sentinel Agents Phase 6 runtime.  To run the API server:

```
uvicorn sentinel_agents.api.main:app --reload
```
"""

from .main import app  # noqa: F401