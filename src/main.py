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
    # initialize workflow state and execute validation/compute steps
    from .workflow import state_graph, WorkflowState

    initial = WorkflowState(
        innings_data={"runs": runs, "balls": balls, "fours": fours, "sixes": sixes},
        output_format=output_format,
    )
    # execute workflow using compiled graph
    from .workflow import compiled_graph

    result_state = compiled_graph.invoke(initial)
    if isinstance(result_state, dict):
        from .workflow import WorkflowState

        result_state = WorkflowState.model_validate(result_state)

    # check for validation errors
    if result_state.validation_errors:
        raise ValueError(result_state.validation_errors[0])

    # convert innings_data back to InningsState if metrics present
    if isinstance(result_state.innings_data, dict):
        state = InningsState.model_validate(result_state.innings_data)
    else:
        state = result_state.innings_data

    return format_summary(state, output_format)
