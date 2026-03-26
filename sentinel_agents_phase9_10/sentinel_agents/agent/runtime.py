"""Agent runtime implementation for Sentinel Agents Phases 9 & 10.

This runtime extends the evaluation and governance flow from Phase 8 by
introducing deployment (Phase 9) and self‑governance (Phase 10).
After executing a task, persisting a trace, learning from it,
computing evaluation metrics and recording an audit entry, the
runtime delegates to the deployment manager to orchestrate the
execution and finally passes the trace to the self‑governance
engine to adapt the policy based on observed behaviour.
"""

from __future__ import annotations

from typing import Any, Dict

from ..policy.policy_engine import PolicyEngine
from ..risk.risk_engine import RiskEngine
from ..memory.memory import MemoryStore
from ..learning.learning_engine import LearningEngine
from ..evaluation.evaluation_engine import EvaluationEngine
from ..governance.governance_engine import GovernanceEngine
from ..deployment.deployment_manager import DeploymentManager
from ..self_governance.self_governance_engine import SelfGovernanceEngine


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
        Computes quality metrics for Phase 7.
    governance_engine : GovernanceEngine
        Records audit logs for Phase 8.
    deployment_manager : DeploymentManager
        Orchestrates multi‑node execution and manages configuration for Phase 9.
    self_governance_engine : SelfGovernanceEngine
        Adapts the policy and risk thresholds based on observed behaviour for Phase 10.

    Notes
    -----
    This runtime executes a single task synchronously.  It is
    intentionally simple and meant to demonstrate the integration of
    deployment and self‑governance layers.  A production system might
    support asynchronous operations, parallel planning, advanced
    orchestration and robust error handling.
    """

    def __init__(
        self,
        policy_engine: PolicyEngine,
        risk_engine: RiskEngine,
        memory_store: MemoryStore,
        learning_engine: LearningEngine,
        evaluation_engine: EvaluationEngine,
        governance_engine: GovernanceEngine,
        deployment_manager: DeploymentManager,
        self_governance_engine: SelfGovernanceEngine,
    ) -> None:
        self.policy_engine = policy_engine
        self.risk_engine = risk_engine
        self.memory_store = memory_store
        self.learning_engine = learning_engine
        self.evaluation_engine = evaluation_engine
        self.governance_engine = governance_engine
        self.deployment_manager = deployment_manager
        self.self_governance_engine = self_governance_engine

    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute a user task under policy, risk, evaluation, deployment and self‑governance.

        Parameters
        ----------
        task : str
            The user‑provided instruction to execute.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the result of execution along with
            risk, evaluation and deployment metadata.  If the task is
            denied at the policy or risk stage, an appropriate status
            is returned.
        """
        # Phase 1–5: policy, risk, execution, memory, learning
        if not self.policy_engine.is_allowed(task):
            return {"status": "denied", "reason": "Policy violation"}

        risk_score = self.risk_engine.score(task)
        if risk_score > self.risk_engine.max_allowed_risk:
            return {"status": "denied", "reason": "Risk too high", "risk": risk_score}

        # Placeholder capability invocation
        result = f"Executed: {task}"

        # Persist execution trace
        trace = {
            "task": task,
            "result": result,
            "risk": risk_score,
        }
        self.memory_store.save_trace(trace)
        trace_id = getattr(self.memory_store, "_next_id", 0) - 1

        # Learning
        self.learning_engine.process(trace)

        # Phase 7: evaluation
        evaluation = self.evaluation_engine.evaluate(trace)

        # Phase 8: governance / audit
        trace_with_id = dict(trace, id=trace_id)
        self.governance_engine.record(trace_with_id)

        # Phase 9: deployment
        deployment_info = self.deployment_manager.deploy(trace_with_id)

        # Phase 10: self‑governance
        self.self_governance_engine.adapt_policy(trace_with_id, evaluation)

        return {
            "status": "success",
            "result": result,
            "risk": risk_score,
            "trace_id": trace_id,
            "evaluation": evaluation,
            "deployment": deployment_info,
        }


def load_default_runtime() -> AgentRuntime:
    """Factory function to construct a default runtime for Phases 9 & 10.

    Creates and wires up the engines for policy, risk, memory, learning,
    evaluation, governance, deployment and self‑governance.  The
    deployment manager reads configuration from `deploy_config.json` if
    it exists and writes log messages; the self‑governance engine uses
    simple heuristics to adjust the policy.

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
    from ..governance.audit_logger import AuditLogger
    audit_logger = AuditLogger("audit.log")
    governance_engine = GovernanceEngine(audit_logger)
    deployment_manager = DeploymentManager("deploy_config.json")
    self_governance_engine = SelfGovernanceEngine(policy_engine, risk_engine)
    return AgentRuntime(
        policy_engine,
        risk_engine,
        memory_store,
        learning_engine,
        evaluation_engine,
        governance_engine,
        deployment_manager,
        self_governance_engine,
    )