"""Learning layer for Sentinel Agents Phase 7 & 8.

This subpackage contains the adaptive learning components introduced in
Phase 6.  The `LearningEngine` orchestrates adaptation and feedback
based on execution traces.  The modules here are unmodified from the
Phase 6 snapshot and serve to demonstrate how learning integrates with
evaluation and governance layers.
"""

from .learning_engine import LearningEngine  # noqa: F401
from .adaptation import Adaptation  # noqa: F401
from .feedback_loop import FeedbackLoop  # noqa: F401

__all__ = ["LearningEngine", "Adaptation", "FeedbackLoop"]