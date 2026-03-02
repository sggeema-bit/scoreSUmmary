"""Metric computation utilities."""

from .innings_state import InningsInput, InningsMetrics


def compute_metrics(input_data: InningsInput) -> InningsMetrics:
    """Compute batting performance metrics from validated input."""

    # Compute strike rate: runs per 100 balls
    strike_rate = (input_data.runs / input_data.balls) * 100

    # Compute boundary percentage
    boundary_runs = (input_data.fours * 4) + (input_data.sixes * 6)
    boundary_percentage = (
        (boundary_runs / input_data.runs * 100) if input_data.runs > 0 else 0.0
    )

    # Compute balls per boundary
    total_boundaries = input_data.fours + input_data.sixes
    balls_per_boundary = (
        input_data.balls / total_boundaries if total_boundaries > 0 else 0.0
    )

    return InningsMetrics(
        strike_rate=round(strike_rate, 2),
        boundary_percentage=round(boundary_percentage, 2),
        balls_per_boundary=round(balls_per_boundary, 2),
    )
