"""Metric computation utilities."""

from .innings_state import InningsInput, InningsMetrics


def compute_metrics(input_data: InningsInput) -> InningsMetrics:
    """Compute batting performance metrics from validated input."""

    # placeholder; actual formulas to be implemented later
    return InningsMetrics(
        strike_rate=0.0,
        boundary_percentage=0.0,
        balls_per_boundary=0.0,
    )
