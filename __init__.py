"""Sentinel Agents package.

This package defines a minimal, governed agent runtime with explicit
capabilities, a simple policy engine and sandbox execution.  It is
intended as an educational example and not a production‑ready system.
\n+It is organised into several subpackages:\n+\n+* ``agent`` – the core agent runtime used to execute prompts under\n+  policy control.\n+* ``policy`` – a graduated policy engine that scores and possibly\n+  modifies actions.\n+* ``memory`` – persistence and recall for agent context.\n+* ``swarm`` – coordination of multiple specialised agents working\n+  together (introduced in Phase 4).\n"""

# Re‑export commonly used classes at the package level for convenience.
from .policy.policy_engine import PolicyEngine  # noqa: F401
from .agent.runtime import run_agent  # noqa: F401
from .swarm import SwarmCoordinator  # noqa: F401
"""
