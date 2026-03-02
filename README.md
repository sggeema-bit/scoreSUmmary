# Batting Metrics Analysis

This repository contains the ScoreSummary Batting Metrics Analysis system. The library computes cricket batting performance metrics from raw innings data using Python and the LangGraph workflow engine.

## Architecture

- **Input validation and state management** are handled by Pydantic models defined in `src/innings_state.py`.
- **Metrics computation** lives in `src/metrics_compute.py`, implementing formulas for strike rate, boundary percentage, and balls‑per‑boundary.
- **Workflow orchestration** uses LangGraph; `src/workflow.py` defines a simple linear state graph that validates input, computes metrics, and finalizes the state.
- **Formatting/output** functions (`src/summary_output.py`) create JSON or human‑readable text summaries.
- **CLI entry point** is provided in `src/cli.py`, exposing the `analyze_innings` function from `src/main.py` as a command‑line tool.

## Development

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -e .
   pip install -e "[dev]"  # for linting/formatting tools
   ```
3. Run tests or try the library interactively by importing `analyze_innings`.
4. Use `ruff` and `black` to lint/format the code according to the configuration in `pyproject.toml`.

See `specs/001-batting-metrics/quickstart.md` for example usage and command‑line options.