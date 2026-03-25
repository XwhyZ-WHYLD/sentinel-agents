"""Sentinel Agents package for Phase 7 and Phase 8.

This package contains the implementation of the Sentinel Agents runtime
extended with an evaluation layer (Phase 7) and a governance layer
(Phase 8).  The structure mirrors that of previous phases but includes
additional modules under `evaluation` and `governance`.

The public API for most users consists of the `AgentRuntime` class in
`agent.runtime` and the FastAPI entrypoint in `api.main`.
"""

__all__ = [
    "agent",
    "api",
    "capabilities",
    "evaluation",
    "governance",
    "learning",
    "memory",
    "policy",
    "risk",
    "sandbox",
    "swarm",
]