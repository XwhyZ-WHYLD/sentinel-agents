"""Capabilities subpackage.

This subpackage would normally expose various external actions such as
HTTP requests, file system access and searching.  In Phase 6 we omit
concrete implementations for brevity.  The agent runtime will need to
extend this package to support additional actions.
"""

__all__: list[str] = []  # no concrete capabilities in this minimal example