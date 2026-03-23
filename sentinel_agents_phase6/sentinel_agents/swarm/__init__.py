"""Swarm subpackage.

Provides a simple `SwarmCoordinator` that can coordinate multiple agents.
The current implementation is intentionally sequential and simplistic to
illustrate how a swarm layer would fit into the architecture.  More
advanced variants could run agents in parallel, assign roles or reach
consensus.
"""

from .swarm_coordinator import SwarmCoordinator  # noqa: F401