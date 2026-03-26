"""Self‑governance engine for Sentinel Agents Phase 10.

This module implements a simple self‑governance mechanism that adapts the
policy and risk thresholds based on observed behaviour.  It is intended
to illustrate how a runtime can evolve its own constraints using
feedback from the evaluation layer.  A production system could use
more sophisticated meta‑learning and policy‑optimization techniques.

Classes
-------
SelfGovernanceEngine
    Adjusts the policy and risk engines in response to evaluation
    results.

"""

from __future__ import annotations

from typing import Dict, Any, Iterable

from ..policy.policy_engine import PolicyEngine
from ..risk.risk_engine import RiskEngine


class SelfGovernanceEngine:
    """A simple self‑governance engine for Phase 10.

    Parameters
    ----------
    policy_engine : PolicyEngine
        The policy engine whose blocked keywords may be updated.
    risk_engine : RiskEngine
        The risk engine whose risk threshold may be adapted.

    Notes
    -----
    This engine uses a heuristic to adapt the system: if a trace has
    non‑zero risk and the evaluation layer marked it as failed, the
    task's words are added to the policy engine's blocked keywords.
    If many tasks are being denied due to risk, the risk threshold is
    gradually lowered.  These simple rules demonstrate how the agent
    could learn to be more conservative over time.
    """

    def __init__(self, policy_engine: PolicyEngine, risk_engine: RiskEngine) -> None:
        self.policy_engine = policy_engine
        self.risk_engine = risk_engine
        # Maintain a counter of denied tasks to adjust risk threshold
        self._denied_count = 0
        self._total_count = 0

    def adapt_policy(self, trace: Dict[str, Any], evaluation: Dict[str, Any]) -> None:
        """Adapt policy and risk thresholds based on a completed trace.

        Parameters
        ----------
        trace : dict
            The execution trace containing at least ``task`` and ``risk``.
        evaluation : dict
            The evaluation results containing at least ``passed`` (bool).

        Notes
        -----
        If the evaluation did not pass and the risk was greater than
        zero, we assume some aspects of the task were unsafe or
        undesirable.  This method then adds individual words from
        the task string to the policy's blocked keywords list.  It
        also tracks the proportion of tasks that are denied and
        gradually lowers the allowed risk threshold if too many tasks
        are deemed high risk.  Conversely, if the pass rate
        improves, the threshold can be relaxed slightly.
        """
        task: str = trace.get("task", "")
        risk: float = float(trace.get("risk", 0))
        passed: bool = bool(evaluation.get("passed", False))

        # Update counters
        self._total_count += 1
        if not passed and risk > 0:
            self._denied_count += 1

            # Extract words from the task as candidate blocked keywords
            words = self._tokenize(task)
            for w in words:
                if w and w not in self.policy_engine.blocked_keywords:
                    self.policy_engine.blocked_keywords.append(w)

        # Adjust risk threshold periodically
        if self._total_count >= 5:
            denial_rate = self._denied_count / self._total_count
            # If more than half the tasks are denied, lower the threshold
            if denial_rate > 0.5:
                self.risk_engine.max_allowed_risk = max(
                    0.1, self.risk_engine.max_allowed_risk - 0.1
                )
            # If very few tasks are denied, relax the threshold slightly
            elif denial_rate < 0.1:
                self.risk_engine.max_allowed_risk = min(
                    1.0, self.risk_engine.max_allowed_risk + 0.05
                )
            # Reset counters
            self._denied_count = 0
            self._total_count = 0

    @staticmethod
    def _tokenize(text: str) -> Iterable[str]:
        """Simple whitespace tokenizer for blocked keyword generation."""
        return [token.strip().lower() for token in text.split()]
