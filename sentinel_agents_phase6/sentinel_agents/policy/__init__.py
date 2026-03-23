"""Policy subpackage.

The policy layer defines rules governing which tasks are permissible.  It
includes a simple `PolicyEngine` class that can be extended with custom
policies and an interface for feeding back adjustments from the learning
layer.
"""

from .policy_engine import PolicyEngine  # noqa: F401