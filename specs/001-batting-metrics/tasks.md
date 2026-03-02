---
description: "Task list for Batting Metrics feature implementation"
---

# Tasks: Batting Metrics Analysis System

**Input**: Design documents from `/specs/001-batting-metrics/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan (src/, docs/, config/)
- [x] T002 Initialize Python project with dependencies LangGraph and Pydantic in pyproject.toml
- [x] T003 [P] Configure linting and formatting tools in ruff.toml/pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Create `src/innings_state.py` and define basic class skeletons for InningsInput, InningsMetrics, InningsState
- [x] T005 [P] Add pyproject.toml metadata and entry points for CLI (`batting_metrics = "src.cli:main"`)
- [x] T006 [P] Create `src/metrics_compute.py` with placeholder compute_metrics function
- [x] T007 [P] Create `src/summary_output.py` with placeholder formatting utilities
- [x] T008 Set up LangGraph workflow boilerplate in `src/workflow.py` (StateGraph, START/END)
- [x] T009 Create `src/cli.py` and `src/main.py` with initial analyze_innings stub
- [x] T010 Configure project packaging and installation instructions (update README or quickstart)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Record Innings Statistics (Priority: P1) 🎯 MVP

**Goal**: Accept and validate innings input state

**Independent Test**: Provide valid and invalid inputs and verify acceptance or rejection

### Implementation for User Story 1

- [x] T011 [P] [US1] Implement `InningsInput` model with fields runs, balls, fours, sixes and validation logic in `src/innings_state.py`
- [x] T012 [US1] Implement `InningsMetrics` model and `InningsState.create_and_compute` factory method in `src/innings_state.py`
- [x] T013 [US1] Add input validation step to workflow graph in `src/workflow.py` (node `validate_input`)
- [x] T014 [US1] Update `analyze_innings` signature in `src/main.py` to accept raw inputs and perform initial state creation

**Checkpoint**: P1 should work alone: validated state created or errors returned

---

## Phase 4: User Story 2 - Compute Derived Metrics (Priority: P2)

**Goal**: Calculate strike rate, boundary percentage, and balls per boundary from validated state

**Independent Test**: Feed known input and compare computed metrics to expected values

### Implementation for User Story 2

- [x] T015 [US2] Implement `compute_metrics` function logic in `src/metrics_compute.py` using formulas from data-model.md
- [x] T016 [US2] Integrate `compute_metrics` into `InningsState.create_and_compute` or workflow step so metrics populate automatically
- [x] T017 [US2] Add workflow node `compute_metrics` and connect it after validation in `src/workflow.py`

**Checkpoint**: Metrics computation works independently when valid state provided

---

## Phase 5: User Story 3 - Generate Performance Summary (Priority: P3)

**Goal**: Produce JSON or text summary output combining inputs and computed metrics

**Independent Test**: Request each format and verify complete data

### Implementation for User Story 3

- [x] T018 [US3] Implement JSON and text formatting functions in `src/summary_output.py`
- [x] T019 [US3] Extend `analyze_innings` to accept `output_format` parameter and return formatted result in `src/main.py`
- [x] T020 [US3] Parse CLI arguments and output summary in `src/cli.py`
- [x] T021 [US3] Update quickstart.md examples to include new CLI commands and format options

**Checkpoint**: Summary generation works and CLI returns correct format

---

## Final Phase: Polish & Cross-Cutting Concerns

- [x] T022 [P] Add module-level docstrings and comments across all src/ files
- [x] T023 [P] Ensure all code passes configured linters/formatters (run ruff/black)
- [x] T024 [P] Update README or docs/architecture.md with final design overview
- [x] T025 [P] Perform code review checklist: clarity, simplicity, standards

**Checkpoint**: Codebase is clean, documented, and ready for production use

---

**Dependencies**: US2 depends on US1, US3 depends on US1 & US2

**Parallel Opportunities**:
- T003, T005, T006, T007, T008, T009 can run concurrently during foundational phase
- US1, US2, US3 tasks can proceed in parallel once foundational tasks complete, with internal dependencies respected

**MVP Scope**: Only User Story 1 (T011–T014) plus foundational setup to deliver basic input & validation

---

Implementation should follow the ScoreSummary Constitution: clear, simple, and well-documented code. Once tasks are executed, the system should be testable via examples described in quickstart.md.
