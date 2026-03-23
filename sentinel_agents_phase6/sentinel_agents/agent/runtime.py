"""Agent runtime implementation for Sentinel Agents Phase 6.

The `AgentRuntime` class defines a minimal loop that processes a user task
through the policy and risk engines, invokes the appropriate capability,
updates the memory, and finally delegates to the learning layer.  This
implementation is intentionally simple to illustrate the integration points
introduced in Phase 6.  In a full system, the planner would break tasks
down into multiple steps and utilise the swarm layer for coordination.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from ..policy.policy_engine import PolicyEngine
from ..risk.risk_engine import RiskEngine
from ..memory.memory import MemoryStore
from ..learning.learning_engine import LearningEngine


class AgentRuntime:
    """Core runtime responsible for executing user tasks.

    Parameters
    ----------
    policy_engine : PolicyEngine
        The policy engine used to evaluate and enforce permissions.
    risk_engine : RiskEngine
        The risk engine used to score potential actions.
    memory_store : MemoryStore
        A persistent store for previous execution traces.
    learning_engine : LearningEngine
        The adaptive learning engine introduced in Phase 6.

    Notes
    -----
    In a production system this runtime would support multi‑step planning,
    asynchronous execution, error handling and advanced logging.  Here we
    implement a simplified, synchronous flow to demonstrate how the
    learning layer plugs into the lifecycle.
    """

    def __init__(
        self,
        policy_engine: PolicyEngine,
        risk_engine: RiskEngine,
        memory_store: MemoryStore,
        learning_engine: LearningEngine,
    ) -> None:
        self.policy_engine = policy_engine
        self.risk_engine = risk_engine
        self.memory_store = memory_store
        self.learning_engine = learning_engine

    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute a user task under policy and risk constraints.

        The method performs the following steps:

        1. Validates the task via the policy engine.
        2. Computes a risk score via the risk engine.
        3. If allowed and within acceptable risk, executes the task via a
           placeholder capability (here we simply echo the task back).
        4. Persists the execution trace to memory.
        5. Passes the trace to the learning engine for adaptive updates.

        Parameters
        ----------
        task : str
            The user‑provided instruction to execute.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the result of execution along with
            diagnostic metadata.
        """
        # Step 1: policy check
        if not self.policy_engine.is_allowed(task):
            return {"status": "denied", "reason": "Policy violation"}

        # Step 2: risk evaluation
        risk_score = self.risk_engine.score(task)
        if risk_score > self.risk_engine.max_allowed_risk:
            return {"status": "denied", "reason": "Risk too high", "risk": risk_score}

        # Step 3: capability invocation (placeholder)
        # In a full system this would dispatch to the appropriate capability
        # such as HTTP, file system or search.  Here we simply echo the task.
        result = f"Executed: {task}"

        # Step 4: persist execution trace
        trace = {
            "task": task,
            "result": result,
            "risk": risk_score,
        }
        self.memory_store.save_trace(trace)

        # Step 5: adaptive learning
        # The learning engine can update memory weighting or feed policy
        # adjustments based on the execution context.
        self.learning_engine.process(trace)

        return {
            "status": "success",
            "result": result,
            "risk": risk_score,
            "trace_id": trace.get("id"),
        }


def load_default_runtime() -> AgentRuntime:
    """Factory function to construct a default runtime.

    This helper assembles the minimal components needed for demonstration
    purposes.  It instantiates a policy engine with permissive defaults, a
    risk engine with a low risk threshold, a JSON‑backed memory store and a
    learning engine that references these components.  Applications can
    customise or extend this factory as needed.

    Returns
    -------
    AgentRuntime
        A ready‑to‑use runtime instance.
    """
    memory_store = MemoryStore("memory.json")
    policy_engine = PolicyEngine()
    risk_engine = RiskEngine(max_allowed_risk=0.5)
    learning_engine = LearningEngine(memory_store, policy_engine)
    return AgentRuntime(policy_engine, risk_engine, memory_store, learning_engine)