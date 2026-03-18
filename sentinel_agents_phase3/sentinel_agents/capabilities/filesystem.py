"""Filesystem capability.

Provides simple functions to read and write text files within a
restricted workspace.  The workspace directory defaults to
``workspace`` at the project root.  Attempts to read or write outside
this directory raise an exception.  This prevents agents from
accessing arbitrary parts of the host filesystem.
"""

from __future__ import annotations

import os
from typing import Any, Optional


WORKSPACE = os.environ.get("SENTINEL_WORKSPACE", os.path.join(os.path.dirname(__file__), "..", "..", "workspace"))


def _ensure_workspace() -> str:
    """Ensure the workspace directory exists and return its absolute path."""
    abs_path = os.path.abspath(WORKSPACE)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path


def _resolve_path(path: str) -> str:
    """Return an absolute path within the workspace.

    Raises ``ValueError`` if the path escapes the workspace root.
    """
    workspace_root = _ensure_workspace()
    abs_path = os.path.abspath(os.path.join(workspace_root, path))
    # Ensure the resolved path begins with the workspace root to avoid path traversal.
    if not abs_path.startswith(workspace_root):
        raise ValueError("Attempted to access path outside workspace")
    return abs_path


def read_file(path: str) -> Any:
    """Read a text file from the workspace.

    Parameters
    ----------
    path: str
        Relative path within the workspace.

    Returns
    -------
    str
        Contents of the file.  Returns an error message if the file
        does not exist or cannot be read.
    """
    try:
        abs_path = _resolve_path(path)
        with open(abs_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        return {"error": str(exc)}


def write_file(path: str, content: str) -> Any:
    """Write content to a file within the workspace.

    Parameters
    ----------
    path: str
        Relative path within the workspace.
    content: str
        Text content to write to the file.

    Returns
    -------
    dict
        A success status or error message.
    """
    try:
        abs_path = _resolve_path(path)
        directory = os.path.dirname(abs_path)
        os.makedirs(directory, exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "written", "path": path}
    except Exception as exc:
        return {"error": str(exc)}
