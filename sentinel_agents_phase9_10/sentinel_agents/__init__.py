"""Sentinel Agents package for Phases 9 & 10.

This package implements the Sentinel Agents runtime extended with
deployment and self‑governance layers.  It includes subpackages for
capabilities, evaluation, governance, learning, memory, policy, risk,
sandbox, swarm, deployment and self‑governance.  Use the
`AgentRuntime` from `agent.runtime` and the FastAPI app in
`api.main` as entrypoints.
"""

__all__ = [
    "agent",
    "api",
    "capabilities",
    "deployment",
    "evaluation",
    "governance",
    "learning",
    "memory",
    "policy",
    "risk",
    "sandbox",
    "self_governance",
    "swarm",
]