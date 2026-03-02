"""LangGraph workflow definition for batting metrics."""

from typing import Optional
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel


class WorkflowState(BaseModel):
    """Workflow state container."""

    messages: list = []
    innings_data: Optional[dict] = None
    validation_errors: list[str] = []
    output_format: str = "json"
    current_step: str = "initialize"


# placeholder graph; to be fleshed out in later tasks
state_graph = StateGraph()

@state_graph.node(START)
def initialize(state: WorkflowState) -> WorkflowState:
    state.current_step = "initialize"
    return state

@state_graph.node()
def validate_input(state: WorkflowState) -> WorkflowState:
    """Validate raw input stored in state.innings_data."

    Expects state.innings_data to be a dict with keys runs, balls, fours, sixes.
    Populates state.validation_errors if any exception occurs.
    """
    from .innings_state import InningsInput

    try:
        InningsInput(**state.innings_data)
    except Exception as exc:  # pylint: disable=broad-except
        state.validation_errors.append(str(exc))
    return state

@state_graph.node(END)
def finalize(state: WorkflowState) -> WorkflowState:
    state.current_step = "final"
    return state
