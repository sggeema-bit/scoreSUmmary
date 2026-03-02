# Data Model: Batting Metrics Analysis

**Date**: 2026-03-02 | **Plan**: [plan.md](plan.md)

## Domain Entities

### InningsState

Represents a single cricket innings with input statistics and computed metrics.

**Purpose**: Central data container for all innings information. Maintains state integrity and coordinates metric computation.

**Input Variables** (captured from user):

| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| `runs` | integer | ≥ 0 | Total runs scored in the innings |
| `balls` | integer | > 0 | Total balls faced (validated > 0 to prevent division by zero) |
| `fours` | integer | ≥ 0 | Count of four-run boundary shots |
| `sixes` | integer | ≥ 0 | Count of six-run boundary shots |

**Derived Variables** (computed automatically):

| Field | Formula | Description | Type |
|-------|---------|-------------|------|
| `strike_rate` | (runs ÷ balls) × 100 | Runs per 100 balls faced | float |
| `boundary_percentage` | ((fours×4+sixes×6) ÷ runs) × 100 | % of runs from boundaries | float |
| `balls_per_boundary` | balls ÷ (fours + sixes) | Avg balls per boundary hit | float |

**Validation Rules**:

1. **Input Validation**
   - `runs`: Must be non-negative integer (≥ 0)
   - `balls`: Must be positive integer (> 0) - rejects 0 to prevent strike_rate calculation error
   - `fours`: Must be non-negative integer (≥ 0)
   - `sixes`: Must be non-negative integer (≥ 0)
   - `(fours + sixes) > 0`: Sum of boundaries must be positive - prevents balls_per_boundary calculation error

2. **Data Integrity** (logical constraints)
   - `runs ≥ 0`: Always valid due to cricket rules
   - `balls ≥ 1`: Enforced by validation rule
   - `fours ≥ 0`: Always valid
   - `sixes ≥ 0`: Always valid
   - Boundary runs must not exceed total runs: `(fours×4 + sixes×6) ≤ runs`
     - Note: If violated, boundary_percentage formula still valid mathematically
     - Flag as warning but allow storage (data input user responsibility)

3. **Invalid Data Rejection** (hard constraints)
   - Reject if `balls = 0` with message: "Balls must be greater than 0 to calculate strike rate"
   - Reject if `(fours + sixes) = 0` with message: "Must have at least one boundary (four or six) to compute metrics"
   - Reject if any input is negative with message: "[field] cannot be negative"

### SummaryOutput

Consolidated output combining all metrics for presentation.

**Purpose**: Generate user-facing output in two formats (JSON and text) with complete information.

**Properties**:

| Field | Value | Description |
|-------|-------|-------------|
| `innings_data` | InningsState | Complete innings object (all input + computed) |
| `timestamp` | datetime | When summary was generated |
| `format_type` | "json" \| "text" | Output format type |

**Output Formats**:

#### JSON Format

```json
{
  "innings": {
    "input": {
      "runs": 50,
      "balls": 40,
      "fours": 3,
      "sixes": 1
    },
    "computed": {
      "strike_rate": 125.0,
      "boundary_percentage": 20.0,
      "balls_per_boundary": 10.0
    }
  },
  "metadata": {
    "generated_at": "2026-03-02T14:30:00Z",
    "valid": true
  }
}
```

#### Text Format

```
═══════════════════════════════════════════════
       BATTING METRICS SUMMARY
═══════════════════════════════════════════════

INPUT STATISTICS
────────────────────────────────────────────
  Runs Scored:                    50
  Balls Faced:                    40
  Four-Run Boundaries:             3
  Six-Run Boundaries:              1

COMPUTED METRICS
────────────────────────────────────────────
  Strike Rate:                   125.0 (runs per 100 balls)
  Boundary Percentage:            20.0% (runs from boundaries)
  Balls Per Boundary:             10.0 (avg balls per boundary)

═══════════════════════════════════════════════
  Generated: 2026-03-02 14:30:00 UTC
═══════════════════════════════════════════════
```

## Pydantic Models

### Core Data Models

```python
# File: src/innings_state.py

from pydantic import BaseModel, Field, validator
from typing import Optional

class InningsInput(BaseModel):
    """Input variables for innings analysis (user-provided data)."""
    
    runs: int = Field(
        ge=0,
        description="Total runs scored in the innings"
    )
    balls: int = Field(
        gt=0,
        description="Total balls faced (must be > 0 to compute strike rate)"
    )
    fours: int = Field(
        ge=0,
        description="Number of four-run boundary shots"
    )
    sixes: int = Field(
        ge=0,
        description="Number of six-run boundary shots"
    )
    
    @validator("balls")
    def validate_balls_not_zero(cls, v):
        """Explicitly validate balls > 0."""
        if v == 0:
            raise ValueError("balls: Balls must be greater than 0 to calculate strike rate")
        return v
    
    @validator("fours", "sixes", always=True)
    def validate_boundaries_sum(cls, v, values):
        """Validate that at least one boundary exists."""
        if "fours" in values and "sixes" in values:
            total_boundaries = values.get("fours", 0) + values.get("sixes", 0)
            if total_boundaries == 0:
                raise ValueError(
                    "Must have at least one boundary (four or six) to compute metrics"
                )
        return v

class InningsMetrics(BaseModel):
    """Computed metrics derived from innings input."""
    
    strike_rate: float = Field(
        description="Runs per 100 balls faced: (runs / balls) * 100"
    )
    boundary_percentage: float = Field(
        description="Percentage of runs from boundaries: ((fours*4 + sixes*6) / runs) * 100"
    )
    balls_per_boundary: float = Field(
        description="Average balls per boundary: balls / (fours + sixes)"
    )

class InningsState(BaseModel):
    """Complete innings state with input and computed metrics."""
    
    input: InningsInput
    metrics: InningsMetrics
    
    @classmethod
    def create_and_compute(cls, runs: int, balls: int, fours: int, sixes: int) -> "InningsState":
        """Factory method: validate input and compute metrics."""
        # Validate input
        input_data = InningsInput(runs=runs, balls=balls, fours=fours, sixes=sixes)
        
        # Compute metrics
        strike_rate = (input_data.runs / input_data.balls) * 100
        boundary_runs = (input_data.fours * 4) + (input_data.sixes * 6)
        boundary_percentage = (boundary_runs / input_data.runs * 100) if input_data.runs > 0 else 0.0
        total_boundaries = input_data.fours + input_data.sixes
        balls_per_boundary = input_data.balls / total_boundaries if total_boundaries > 0 else 0.0
        
        metrics = InningsMetrics(
            strike_rate=round(strike_rate, 2),
            boundary_percentage=round(boundary_percentage, 2),
            balls_per_boundary=round(balls_per_boundary, 2)
        )
        
        return cls(input=input_data, metrics=metrics)

class SummaryOutputData(BaseModel):
    """Complete summary output combining input and metrics."""
    
    innings: InningsState
    generated_at: str = Field(description="ISO 8601 timestamp of generation")
    valid: bool = Field(default=True, description="Whether innings data is valid")
```

## State Transitions

### LangGraph Workflow State

```python
# File: src/workflow.py

from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import BaseMessage

class WorkflowState(BaseModel):
    """State for LangGraph workflow."""
    
    messages: Annotated[list[BaseMessage], operator.add] = []
    innings_data: Optional[InningsState] = None
    validation_errors: list[str] = []
    output_format: Literal["json", "text"] = "json"
    current_step: str = "initialize"
```

### State Machine Flow

```
START
  ↓
INPUT VALIDATION
  ├─ Valid? → COMPUTE METRICS
  │           ↓
  │        GENERATE SUMMARY
  │           ↓
  │        OUTPUT (JSON/TEXT)
  │           ↓
  │          END
  │
  └─ Invalid? → COLLECT ERRORS → END
```

## Metric Computation

### Formula Definitions

**Strike Rate** (runs per 100 balls)
```
strike_rate = (runs ÷ balls) × 100
Example: 50 runs in 40 balls = (50/40) × 100 = 125.0 runs per 100 balls
```

**Boundary Percentage** (% of runs from boundaries)
```
boundary_runs = (fours × 4) + (sixes × 6)
boundary_percentage = (boundary_runs ÷ runs) × 100
Example: 3 fours + 1 six = 12+6 = 18 runs from boundaries out of 50 total = (18/50) × 100 = 36.0%
```

**Balls Per Boundary** (average balls per boundary hit)
```
total_boundaries = fours + sixes
balls_per_boundary = balls ÷ total_boundaries
Example: 40 balls with 4 boundaries = 40/4 = 10.0 balls per boundary
```

### Computation Logic

```python
# File: src/metrics_compute.py

def compute_metrics(input_data: InningsInput) -> InningsMetrics:
    """Compute all metrics from validated input."""
    
    # Strike rate: (runs / balls) * 100
    strike_rate = (input_data.runs / input_data.balls) * 100
    
    # Boundary percentage
    boundary_runs = (input_data.fours * 4) + (input_data.sixes * 6)
    boundary_percentage = (
        (boundary_runs / input_data.runs * 100) 
        if input_data.runs > 0 
        else 0.0
    )
    
    # Balls per boundary
    total_boundaries = input_data.fours + input_data.sixes
    balls_per_boundary = (
        input_data.balls / total_boundaries 
        if total_boundaries > 0 
        else 0.0
    )
    
    return InningsMetrics(
        strike_rate=round(strike_rate, 2),
        boundary_percentage=round(boundary_percentage, 2),
        balls_per_boundary=round(balls_per_boundary, 2)
    )
```

## Edge Cases & Handling

| Edge Case | Input | Handling | Output |
|-----------|-------|----------|--------|
| No boundaries | fours=0, sixes=0 | Reject at validation | Error message |
| Zero balls | balls=0 | Reject at validation | Error message |
| No runs | runs=0 | Compute, boundary_percentage=0 | Valid |
| Impossible data* | runs < boundary_runs | Warning flag, compute anyway | Valid with flag |
| All sixes | fours=0, sixes=N | Valid | Computed correctly |
| All fours | fours=N, sixes=0 | Valid | Computed correctly |

*Impossible data example: runs=10, fours=2, sixes=0 → boundary_runs=(2×4)=8 which is < 10, so valid. But if sixes=2 → boundary_runs=2×6=12 which is > 10 (impossible in cricket).

---

**Version**: 1.0.0 | **Status**: Design Complete
