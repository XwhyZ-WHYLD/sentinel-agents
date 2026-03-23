"""Learning subpackage (Phase 6).

This subpackage introduces the adaptive learning layer for Sentinel Agents.
It contains three key modules:

* `learning_engine.py` – orchestrates learning across executions and
  coordinates with memory and policy layers.
* `feedback_loop.py` – encapsulates the logic for feeding execution
  outcomes back into the system.
* `adaptation.py` – provides simple adaptation algorithms for adjusting
  memory weights and policy restrictions.
"""

from .learning_engine import LearningEngine  # noqa: F401
from .feedback_loop import FeedbackLoop  # noqa: F401
from .adaptation import Adaptation  # noqa: F401