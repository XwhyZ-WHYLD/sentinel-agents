"""Simple swarm coordinator for Sentinel Agents.

Phase 4 of the Sentinel project introduces the ability to run
multiple specialised agents in parallel and aggregate their results.
This module implements a basic coordinator that takes a collection
of roles, prefixes each role with customised instructions and then
dispatches the tasks to the existing agent runtime.  The
coordinator collects the individual answers and logs and returns
a combined summary.

The design emphasises simplicity: each role runs sequentially in
this implementation; you could extend this to true parallelism via
threads or async execution.  The coordinator does not enforce any
particular consensus mechanism – instead it returns all agent
outputs for higher‑level decision making, which could include
voting, ranking or heuristic selection.

Example
-------

::

    from sentinel_agents.policy.policy_engine import PolicyEngine
    from sentinel_agents.swarm.coordinator import SwarmCoordinator

    roles = {
        "Planner": "As a planning agent, break the task into high‑level steps.",
        "Coder": "As a coding agent, implement any code required.",
        "Tester": "As a testing agent, verify the output and spot errors."
    }
    policy = PolicyEngine()
    coordinator = SwarmCoordinator(roles)
    result = coordinator.run_swarm(
        prompt="Create a function that computes Fibonacci numbers.",
        permissions={"filesystem": True, "network": False},
        policy=policy,
    )
    print(result["answer"])

"""

from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Optional, Tuple

from ..agent.runtime import run_agent
from ..policy.policy_engine import PolicyEngine


class SwarmCoordinator:
    """Coordinate multiple specialised agents and merge their responses.

    Parameters
    ----------
    roles:
        A mapping from role name to a prompt prefix for that role.  The
        prefix should contain any special instructions you want the
        agent to follow.  For example ``{"Planner": "As a planning
        agent"}``.
    default_permissions:
        A dictionary of default permissions to pass to each agent
        invocation.  You can override this per call via
        :meth:`run_swarm`.

    Notes
    -----
    The coordinator uses the existing :func:`sentinel_agents.agent.runtime.run_agent`
    function for each agent.  It does not enforce concurrency; agents
    are executed sequentially.  The outputs are returned as a
    dictionary keyed by role name.  A simple combined answer is
    produced by concatenating each agent's answer with a header.
    """

    def __init__(self, roles: Mapping[str, str], default_permissions: Optional[Mapping[str, bool]] = None) -> None:
        if not roles:
            raise ValueError("SwarmCoordinator requires at least one role")
        self.roles: Dict[str, str] = dict(roles)
        self.default_permissions: Dict[str, bool] = dict(default_permissions or {})

    def run_swarm(
        self,
        prompt: str,
        permissions: Optional[Mapping[str, bool]] = None,
        policy: Optional[PolicyEngine] = None,
        metadata: Optional[Mapping[str, str]] = None,
    ) -> Dict[str, object]:
        """Execute the prompt using all configured roles and aggregate results.

        Parameters
        ----------
        prompt:
            The base prompt or instruction that should be given to each
            agent.  The coordinator will prepend each role's prefix to
            this prompt.
        permissions:
            Permissions to use for this run.  If omitted, the
            ``default_permissions`` passed to the constructor are used.
        policy:
            An optional policy engine.  If provided, this policy will
            be used for all agent invocations.  Otherwise a new
            :class:`PolicyEngine` instance is created for each agent.
        metadata:
            Optional metadata to attach to each agent run.  This value is
            passed through to :func:`run_agent`.

        Returns
        -------
        dict
            A dictionary with the following keys:

            ``answer``: A combined answer summarising each agent's output.
            ``roles``: A mapping from role name to the answer produced
            by that role.
            ``logs``: A list containing the logs from each agent run.
        """
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non‑empty string")
        # Resolve permissions
        merged_permissions: Dict[str, bool] = dict(self.default_permissions)
        if permissions:
            merged_permissions.update(permissions)
        # Use provided policy or create a fresh one
        policy_engine: PolicyEngine = policy or PolicyEngine()

        role_answers: Dict[str, str] = {}
        logs: List[Mapping[str, object]] = []
        # Dispatch each role sequentially
        for role_name, prefix in self.roles.items():
            role_prompt = f"{prefix}\n\n{prompt}".strip()
            # Run the agent
            result = run_agent(
                prompt=role_prompt,
                agent_name=role_name,
                permissions=merged_permissions,
                policy=policy_engine,
                metadata=metadata,
            )
            # Extract answer and log
            role_answer = result.get("answer", "")
            role_answers[role_name] = role_answer
            logs.append({role_name: result.get("logs")})
        # Combine answers into a summary
        combined_parts: List[str] = []
        for role, answer_text in role_answers.items():
            header = f"## {role}" if len(self.roles) > 1 else role
            combined_parts.append(f"{header}\n{answer_text}".strip())
        combined_answer = "\n\n".join(combined_parts)
        return {
            "answer": combined_answer,
            "roles": role_answers,
            "logs": logs,
        }


__all__ = ["SwarmCoordinator"]
