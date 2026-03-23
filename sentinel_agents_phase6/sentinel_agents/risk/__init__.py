"""Risk subpackage.

The risk module provides a simple `RiskEngine` that assigns a numeric
risk score to a task.  The default scoring mechanism is naive—it assigns
risk based on the presence of certain risky keywords.  In a production
implementation, this module would incorporate more sophisticated
heuristics or machine learning models.
"""

from .risk_engine import RiskEngine  # noqa: F401