"""Swarm coordination for multi-agent execution.

This package implements a simple multi‑agent orchestration layer for
Sentinel Agents.  It provides classes for coordinating several
specialised agents – such as planners, coders and testers – and
merging their outputs into a single response.  These components form
the foundation of **phase 4** of the Sentinel project, which
introduces emergent intelligence through collaboration.

The main entry point is :class:`~sentinel_agents.swarm.coordinator.SwarmCoordinator`.
"""

from .coordinator import SwarmCoordinator  # noqa: F401
