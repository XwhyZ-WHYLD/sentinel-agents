"""Deployment layer for Sentinel Agents Phase 9.

Exports the configuration loader and deployment manager.  The
deployment layer orchestrates the runtime across multiple nodes and
reads configuration data.  In this reference implementation the
deployment manager simply records deployment events and returns a
message; no real orchestration occurs.
"""

from .deployment_manager import DeploymentManager  # noqa: F401
from .config import DeploymentConfig  # noqa: F401

__all__ = ["DeploymentManager", "DeploymentConfig"]