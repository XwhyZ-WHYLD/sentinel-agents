"""FastAPI server exposing the agent runtime."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ..agent.runtime import run_agent
from ..policy.policy_engine import PolicyEngine


app = FastAPI(title="Sentinel Agents API", description="Run governed AI agents", version="0.1.0")


class RunRequest(BaseModel):
    agent: str = Field(..., description="Name of the agent (for logs)")
    prompt: str = Field(..., description="The user’s request or instruction")
    permissions: List[str] = Field(..., description="List of capability names the agent may use")


class RunResponse(BaseModel):
    answer: str
    logs: List[Dict[str, Any]]


@app.post("/run", response_model=RunResponse)
async def run(request: RunRequest) -> RunResponse:
    """Execute the agent with the given prompt and permissions."""
    if not request.permissions:
        raise HTTPException(status_code=400, detail="permissions list cannot be empty")
    policy = PolicyEngine(request.permissions)
    result = run_agent(request.prompt, request.agent, request.permissions, policy)
    return RunResponse(answer=result.get("answer", ""), logs=result.get("logs", []))
