"""Summary output formatting functions."""

from typing import Literal
from .innings_state import InningsState


def format_json(state: InningsState) -> str:
    """Return JSON representation of the innings state."""
    return state.model_dump_json(indent=2)


def format_text(state: InningsState) -> str:
    """Return human-readable text summary of the innings state.

    The layout is organized into input statistics followed by computed metrics.
    This mirrors the JSON structure but with labels and simple separators for
    readability in a terminal or report.
    """
    lines: list[str] = []
    lines.append("═══════════════════════════════════════════════════════")
    lines.append("       BATTING METRICS SUMMARY")
    lines.append("═══════════════════════════════════════════════════════")
    lines.append("")
    lines.append("INPUT STATISTICS")
    lines.append("───────────────────────────────────────────────────────")
    lines.append(f"  Runs Scored:               {state.input.runs}")
    lines.append(f"  Balls Faced:               {state.input.balls}")
    lines.append(f"  Four-Run Boundaries:       {state.input.fours}")
    lines.append(f"  Six-Run Boundaries:        {state.input.sixes}")
    lines.append("")
    lines.append("COMPUTED METRICS")
    lines.append("───────────────────────────────────────────────────────")
    lines.append(f"  Strike Rate:              {state.metrics.strike_rate:.2f} (runs per 100 balls)")
    lines.append(f"  Boundary Percentage:      {state.metrics.boundary_percentage:.2f}%")
    lines.append(f"  Balls Per Boundary:       {state.metrics.balls_per_boundary:.2f}")
    lines.append("")
    lines.append("═══════════════════════════════════════════════════════")
    return "\n".join(lines)


def format_summary(state: InningsState, output_format: Literal["json", "text"]) -> str:
    if output_format == "json":
        return format_json(state)
    else:
        return format_text(state)
