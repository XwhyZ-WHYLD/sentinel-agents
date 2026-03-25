"""FastAPI application for Sentinel Agents Phases 9 & 10.

This API exposes a single `/execute` endpoint that accepts a JSON
payload with a `task` field.  It uses a default `AgentRuntime`
constructed via `load_default_runtime` to process the task.  The
response includes the execution status, risk score, evaluation
metrics, deployment metadata and trace identifier.  An audit log is
written to `audit.log` and the policy may evolve over time through
self‑governance.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..agent.runtime import load_default_runtime, AgentRuntime


class ExecuteRequest(BaseModel):
    """Request model for executing a task."""
    task: str


class ExecuteResponse(BaseModel):
    """Response model for task execution results."""
    status: str
    result: str | None = None
    risk: float | None = None
    trace_id: int | None = None
    evaluation: dict[str, float | bool] | None = None
    deployment: dict[str, str] | None = None
    reason: str | None = None


app = FastAPI(title="Sentinel Agents Phases 9 & 10 API")

# Instantiate a single runtime for this API instance.
runtime_instance: AgentRuntime = load_default_runtime()


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest) -> ExecuteResponse:
    """Execute a task via the Sentinel Agents runtime."""
    if not request.task:
        raise HTTPException(status_code=400, detail="Task must not be empty")
    result = runtime_instance.execute_task(request.task)
    return ExecuteResponse(**result)