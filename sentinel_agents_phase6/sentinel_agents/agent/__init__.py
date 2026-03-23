"""Agent subpackage.

This subpackage defines the core agent runtime for executing tasks under the
Sentinel Agents architecture.  The runtime consults the policy and risk
engines before executing actions via the capabilities layer and feeds
execution results into the adaptive learning layer introduced in Phase 6.
"""

from .runtime import AgentRuntime  # noqa: F401