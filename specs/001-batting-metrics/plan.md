# Implementation Plan: Batting Metrics Analysis System

**Branch**: `001-batting-metrics` | **Date**: 2026-03-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-batting-metrics/spec.md`

## Summary

The Batting Metrics Analysis System maintains cricket innings state with input variables (runs, balls, fours, sixes) and computes derived performance metrics (strike_rate, boundary_percentage, balls_per_boundary). The system validates input data, computes metrics using mathematical formulas, and generates summary output in JSON and human-readable text formats. Implementation uses LangGraph as the state management and workflow orchestration framework, enabling clear state transitions and metric computation logic.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: LangGraph (state management & workflows), Pydantic (data validation), JSON (structured output)  
**Storage**: In-memory state (no persistence layer required)  
**Testing**: Optional (per ScoreSummary Constitution - no testing required)  
**Target Platform**: Python command-line application / library  
**Project Type**: Library with CLI wrapper  
**Performance Goals**: Not required (per Constitution)  
**Constraints**: None specified  
**Scale/Scope**: Single innings analysis; supports multiple innings sequentially  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Principles Compliance**:

✅ **I. Code Clarity & Readability**
- Clear input validation error messages
- Self-documenting code structure with type hints (Pydantic models)
- Explicit state transitions and metric computation logic
- No cryptic calculations; formulas broken into named intermediate values
- **Status**: Passed

✅ **II. Simplicity & Minimal Complexity**
- Three primary user stories (P1: input, P2: compute, P3: summary)
- Minimal dependencies (LangGraph, Pydantic only)
- No over-engineered architecture; direct state-to-output flow
- No unnecessary abstraction layers
- **Status**: Passed

✅ **III. Consistency & Code Standards**
- Consistent naming: snake_case for variables, PascalCase for classes
- Linter/formatter configuration required (Black, Ruff)
- Uniform error handling across all input paths
- **Status**: Passed

✅ **IV. Comprehensive Documentation**
- Function/method documentation for all public APIs
- Module-level documentation explaining state flow
- Architecture decisions documented in data-model.md
- **Status**: Passed

✅ **V. Code Review & Knowledge Transfer**
- Mandatory peer review before merge
- Clear PR descriptions required
- Code review focus: clarity and maintainability
- **Status**: Passed

**No violations identified. Plan approved for Phase 0.**

## Project Structure

### Documentation (this feature)

```text
specs/001-batting-metrics/
├── plan.md                      # This file
├── research.md                  # Phase 0 output
├── data-model.md                # Phase 1 output
├── quickstart.md                # Phase 1 output
├── contracts/
│   └── innings_contract.md      # Phase 1 output
├── spec.md                       # Feature specification
└── checklists/
    └── requirements.md          # Quality validation
```

### Source Code (repository root)

```text
src/
├── innings_state.py             # Core InningsState model (Pydantic)
├── metrics_compute.py           # Metric computation logic
├── validation.py                # Input validation rules
├── summary_output.py            # Summary generation (JSON & text)
├── workflow.py                  # LangGraph state graph & workflow
├── cli.py                       # Command-line interface
└── main.py                      # Entry point / API

docs/
├── architecture.md              # Design decisions & rationale
└── examples.md                  # Usage examples

config/
├── pyproject.toml              # Project metadata & dependencies
├── ruff.toml                   # Linting configuration
├── pyproject.toml             # Format configuration

tests/ (OPTIONAL per Constitution)
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single project layout with clear module separation. Core logic in separate modules (state, validation, computation, output) orchestrated by LangGraph workflow. CLI wrapper provides user interface.

## Complexity Tracking

> **No violations requiring justification. Constitution fully compliant.**

All implementation decisions follow simplicity principle. LangGraph chosen specifically for:
- Clear state transitions and workflows (not over-engineered)
- Pythonic approach matching Python 3.11+ ecosystem
- Built-in state management preventing boilerplate
- Minimal learning curve for developers

## Phase 0: Research & Clarifications

### Research Executed

**Topic 1: LangGraph State Management Best Practices**
- LangGraph `StateGraph` pattern for workflow orchestration
- State validation integration with Pydantic models
- Reducer patterns for state updates
- Error handling and recovery mechanisms

**Topic 2: Input Validation Strategy for Cricket Metrics**
- Non-negative integer validation
- Constraint validation (e.g., fours, sixes relationships)
- Error message clarity and user guidance
- Rejection vs. correction trade-offs

**Topic 3: Output Format Generation (JSON & Text)**
- Pydantic `model_dump_json()` for JSON serialization
- Template-based text formatting for readability
- Precision handling for floating-point metrics
- Format consistency across outputs

### All Clarifications RESOLVED

**Q1: Division by zero (balls = 0)** → Reject with clear error (input validation)
**Q2: No boundaries (fours + sixes = 0)** → Reject with clear error (input validation)

## Phase 1: Design Documents

### Data Model

See [data-model.md](data-model.md) for:
- InningsState entity definition
- Computed metric formulas
- Validation rules
- State transitions
- Pydantic model schemas

### API Contracts

See [contracts/innings_contract.md](contracts/innings_contract.md) for:
- Input contract: accepted variable formats and constraints
- Output contract: JSON schema and text format specification
- Error contract: error codes and messages
- State contract: intermediate state visibility

### Quick Start Guide

See [quickstart.md](quickstart.md) for:
- Installation instructions
- Basic library usage example
- CLI interface examples
- Common use cases

## Phase 2: Implementation Tasks (NEXT PHASE)

> Tasks are generated by `/speckit.tasks` command based on user stories. Run:
> ```
> /speckit.tasks 001-batting-metrics
> ```

Expected task phases:
1. **Foundational**: Project setup, dependencies, linting configuration
2. **P1 Tasks**: InningsState model, validation logic
3. **P2 Tasks**: Metric computation, formula implementation
4. **P3 Tasks**: Summary generation, CLI interface

---

**Version**: 1.0.0 | **Status**: Phase 1 Design Complete | **Next**: Generate data-model.md, contracts, quickstart.md
