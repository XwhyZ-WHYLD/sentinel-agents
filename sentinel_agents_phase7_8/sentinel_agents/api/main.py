"""FastAPI application for Sentinel Agents Phase 7 & 8.

This API exposes a single endpoint, `/execute`, that accepts a JSON
payload with a `task` field.  It uses a default `AgentRuntime`
constructed via `load_default_runtime` to process the task.  The result
includes the execution status, output, risk score, evaluation metrics
and trace identifier.  The audit log is written to `audit.log` in the
current working directory.
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
    reason: str | None = None


app = FastAPI(title="Sentinel Agents Phase 7 & 8 API")

# Instantiate a single runtime for this API instance.
runtime_instance: AgentRuntime = load_default_runtime()


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest) -> ExecuteResponse:
    """Execute a task via the Sentinel Agents runtime."""
    if not request.task:
        raise HTTPException(status_code=400, detail="Task must not be empty")
    result = runtime_instance.execute_task(request.task)
    return ExecuteResponse(**result)