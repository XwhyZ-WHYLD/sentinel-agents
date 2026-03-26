"""Configuration handling for the deployment layer.

The `DeploymentConfig` class loads deployment configuration from a
JSON file.  The configuration may specify nodes, API gateway
endpoints or other deployment parameters.  This class is minimal and
intended to illustrate how configuration could be integrated into the
runtime.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


class DeploymentConfig:
    """Load deployment configuration from a JSON file."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from file if it exists."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}
        except json.JSONDecodeError:
            self.config = {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Return a configuration value or default if not present."""
        return self.config.get(key, default)