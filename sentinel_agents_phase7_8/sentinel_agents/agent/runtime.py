"""Agent runtime implementation for Sentinel Agents Phase 7 & 8.

This runtime extends the Phase 6 loop by integrating two additional
layers:

* **Evaluation** (Phase 7) – compute a simple quality score and
  determine whether the execution passed basic criteria.  This is
  represented by the `EvaluationEngine`.

* **Governance & Audit** (Phase 8) – record an audit log of every
  execution trace.  The `GovernanceEngine` writes a JSON line to a
  log file, providing traceability and a foundation for future
  compliance features.

The core flow remains: policy check → risk scoring → capability
execution → memory persistence → learning → evaluation → governance.
"""

from __future__ import annotations

from typing import Any, Dict

from ..policy.policy_engine import PolicyEngine
from ..risk.risk_engine import RiskEngine
from ..memory.memory import MemoryStore
from ..learning.learning_engine import LearningEngine
from ..evaluation.evaluation_engine import EvaluationEngine
from ..governance.governance_engine import GovernanceEngine


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
        The adaptive learning engine from Phase 6.
    evaluation_engine : EvaluationEngine
        The engine computing metrics and success/failure for Phase 7.
    governance_engine : GovernanceEngine
        The audit and governance engine for Phase 8.

    Notes
    -----
    This runtime is intentionally simple.  It executes a single task
    synchronously and does not attempt multi‑step planning or error
    recovery.  The goal is to illustrate how the new layers fit into
    the lifecycle.
    """

    def __init__(
        self,
        policy_engine: PolicyEngine,
        risk_engine: RiskEngine,
        memory_store: MemoryStore,
        learning_engine: LearningEngine,
        evaluation_engine: EvaluationEngine,
        governance_engine: GovernanceEngine,
    ) -> None:
        self.policy_engine = policy_engine
        self.risk_engine = risk_engine
        self.memory_store = memory_store
        self.learning_engine = learning_engine
        self.evaluation_engine = evaluation_engine
        self.governance_engine = governance_engine

    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute a user task under policy, risk, evaluation and governance.

        Steps:

        1. Validate the task via the policy engine.
        2. Compute a risk score via the risk engine.
        3. If allowed and within acceptable risk, execute the task via a
           placeholder capability (here we simply echo the task back).
        4. Persist the execution trace to memory.
        5. Pass the trace to the learning engine for adaptive updates.
        6. Evaluate the trace (Phase 7) to compute a quality score.
        7. Record the trace in the audit log (Phase 8).

        Parameters
        ----------
        task : str
            The user‑provided instruction to execute.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the result of execution along with
            risk and evaluation metadata.  If the task is denied at the
            policy or risk stage, an appropriate status is returned.
        """
        # Step 1: policy check
        if not self.policy_engine.is_allowed(task):
            return {"status": "denied", "reason": "Policy violation"}

        # Step 2: risk evaluation
        risk_score = self.risk_engine.score(task)
        if risk_score > self.risk_engine.max_allowed_risk:
            return {"status": "denied", "reason": "Risk too high", "risk": risk_score}

        # Step 3: capability invocation (placeholder)
        result = f"Executed: {task}"

        # Step 4: persist execution trace
        trace = {
            "task": task,
            "result": result,
            "risk": risk_score,
        }
        # Save the trace; this will assign an identifier internally.  The
        # trace object passed to `save_trace` is not mutated, so the id
        # must be retrieved from the memory store after saving.
        self.memory_store.save_trace(trace)

        # Retrieve the assigned trace id: it will be the last saved id.
        # We assume `_next_id` has been incremented by one.  This is a
        # simple workaround for exposing the identifier without changing
        # the `MemoryStore` API.
        trace_id = getattr(self.memory_store, "_next_id", 0) - 1

        # Step 5: adaptive learning
        self.learning_engine.process(trace)

        # Step 6: evaluation
        evaluation = self.evaluation_engine.evaluate(trace)

        # Step 7: governance / audit
        # Augment the trace with its identifier before recording
        trace_with_id = dict(trace, id=trace_id)
        self.governance_engine.record(trace_with_id)

        # Return aggregated response
        return {
            "status": "success",
            "result": result,
            "risk": risk_score,
            "trace_id": trace_id,
            "evaluation": evaluation,
        }


def load_default_runtime() -> AgentRuntime:
    """Factory function to construct a default runtime for Phase 7 & 8.

    This helper assembles the minimal components needed for demonstration
    purposes.  It instantiates a policy engine with permissive defaults, a
    risk engine with a moderate risk threshold, a JSON‑backed memory store,
    a learning engine, an evaluation engine and a governance engine.  The
    audit logger writes to `audit.log` in the current working directory.

    Returns
    -------
    AgentRuntime
        A ready‑to‑use runtime instance.
    """
    memory_store = MemoryStore("memory.json")
    policy_engine = PolicyEngine()
    risk_engine = RiskEngine(max_allowed_risk=0.5)
    learning_engine = LearningEngine(memory_store, policy_engine)
    evaluation_engine = EvaluationEngine(memory_store, risk_engine)
    from ..governance.audit_logger import AuditLogger  # imported here to avoid cycles

    audit_logger = AuditLogger("audit.log")
    governance_engine = GovernanceEngine(audit_logger)
    return AgentRuntime(
        policy_engine,
        risk_engine,
        memory_store,
        learning_engine,
        evaluation_engine,
        governance_engine,
    )