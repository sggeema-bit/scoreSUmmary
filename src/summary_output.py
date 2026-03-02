"""Summary output formatting functions."""

from typing import Literal
from .innings_state import InningsState


def format_json(state: InningsState) -> str:
    """Return JSON representation of the innings state."""
    return state.model_dump_json(indent=2)


def format_text(state: InningsState) -> str:
    """Return human-readable text summary of the innings state."""
    # simple placeholder
    return str(state)


def format_summary(state: InningsState, output_format: Literal["json", "text"]) -> str:
    if output_format == "json":
        return format_json(state)
    else:
        return format_text(state)
