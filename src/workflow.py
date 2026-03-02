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


# build a simple workflow graph using LangGraph APIs
state_graph = StateGraph(state_schema=WorkflowState)


def initialize(state: WorkflowState) -> WorkflowState:
    state.current_step = "initialize"
    return state


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


def compute_metrics_node(state: WorkflowState) -> WorkflowState:
    """Compute metrics and attach to innings_data if validation passed."""
    if state.validation_errors:
        return state
    from .innings_state import InningsState

    state.innings_data = InningsState.create_and_compute(**state.innings_data).model_dump()
    return state


def finalize(state: WorkflowState) -> WorkflowState:
    state.current_step = "final"
    return state

# add nodes to graph and specify entry/exit
state_graph.add_node("initialize", initialize)
state_graph.add_node("validate_input", validate_input)
state_graph.add_node("compute_metrics", compute_metrics_node)
state_graph.add_node("finalize", finalize)

state_graph.set_entry_point("initialize")
state_graph.set_finish_point("finalize")

# connect edges in simple linear flow
state_graph.add_edge("initialize", "validate_input")
state_graph.add_edge("validate_input", "compute_metrics")
state_graph.add_edge("compute_metrics", "finalize")

# compile graph once for execution
compiled_graph = state_graph.compile()
