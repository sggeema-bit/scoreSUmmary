"""Main entry point for batting metrics library."""

from typing import Literal
from .innings_state import InningsState
from .summary_output import format_summary


def analyze_innings(
    runs: int,
    balls: int,
    fours: int,
    sixes: int,
    output_format: Literal["json", "text"] = "json",
) -> str | dict:
    """Analyze batting metrics for a cricket innings.

    Stub implementation; will validate input via InningsState and generate
    output once metrics computation is implemented.
    """
    # create state (validation occurs in InningsInput)
    state = InningsState.create_and_compute(runs, balls, fours, sixes)
    return format_summary(state, output_format)
