# API Contracts: Batting Metrics Analysis

**Date**: 2026-03-02 | **Data Model**: [data-model.md](../data-model.md)

## Input Contract

**Purpose**: Define what input the system accepts and validation rules.

### Valid Input Format

```python
{
    "runs": int,      # ≥ 0, total runs scored
    "balls": int,     # > 0, total balls faced (MUST be positive)
    "fours": int,     # ≥ 0, number of four-run boundaries
    "sixes": int      # ≥ 0, number of six-run boundaries
}
```

### Input Constraints

| Field | Type | Min | Max | Required | Example | Error if violated |
|-------|------|-----|-----|----------|---------|------------------|
| runs | integer | 0 | Unlimited | Yes | 50 | "runs cannot be negative" |
| balls | integer | 1 | Unlimited | Yes | 40 | "balls must be greater than 0" |
| fours | integer | 0 | unlimited | Yes | 3 | "fours cannot be negative" |
| sixes | integer | 0 | Unlimited | Yes | 1 | "sixes cannot be negative" |
| Boundaries | sum | 1 | Unlimited | Yes | 4 | "Must have at least one boundary" |

### Example Valid Inputs

**Example 1: Standard Innings**
```json
{
    "runs": 75,
    "balls": 60,
    "fours": 4,
    "sixes": 2
}
```
Status: ✅ Valid

**Example 2: All Fours**
```json
{
    "runs": 48,
    "balls": 24,
    "fours": 12,
    "sixes": 0
}
```
Status: ✅ Valid

### Example Invalid Inputs

**Example 1: Zero Balls (Division by Zero)**
```json
{
    "runs": 50,
    "balls": 0,
    "fours": 3,
    "sixes": 1
}
```
Status: ❌ Rejected
Error: "balls must be greater than 0 to calculate strike rate"

**Example 2: No Boundaries**
```json
{
    "runs": 50,
    "balls": 40,
    "fours": 0,
    "sixes": 0
}
```
Status: ❌ Rejected
Error: "Must have at least one boundary (four or six) to compute metrics"

**Example 3: Negative Values**
```json
{
    "runs": -10,
    "balls": 40,
    "fours": 3,
    "sixes": 1
}
```
Status: ❌ Rejected
Error: "runs cannot be negative"

---

## Output Contract

**Purpose**: Define what output the system produces and format specifications.

### Output Format Types

The system supports two output formats:

#### 1. JSON Output Format

**Schema**:
```json
{
    "innings": {
        "input": {
            "runs": integer,
            "balls": integer,
            "fours": integer,
            "sixes": integer
        },
        "metrics": {
            "strike_rate": float,
            "boundary_percentage": float,
            "balls_per_boundary": float
        }
    },
    "metadata": {
        "generated_at": "ISO 8601 timestamp",
        "valid": boolean
    }
}
```

**Example**:
```json
{
    "innings": {
        "input": {
            "runs": 50,
            "balls": 40,
            "fours": 3,
            "sixes": 1
        },
        "metrics": {
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

#### 2. Text Output Format

**Structure**: Human-readable formatted text with clear sections and labels.

**Template**:
```
═══════════════════════════════════════════════
       BATTING METRICS SUMMARY
═══════════════════════════════════════════════

INPUT STATISTICS
────────────────────────────────────────────
  Runs Scored:                    {runs}
  Balls Faced:                    {balls}
  Four-Run Boundaries:             {fours}
  Six-Run Boundaries:              {sixes}

COMPUTED METRICS
────────────────────────────────────────────
  Strike Rate:                   {strike_rate} (runs per 100 balls)
  Boundary Percentage:            {boundary_percentage}% (runs from boundaries)
  Balls Per Boundary:             {balls_per_boundary} (avg balls per boundary)

═══════════════════════════════════════════════
  Generated: {generated_at}
═══════════════════════════════════════════════
```

**Example**:
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

### Output Guarantees

| Guarantee | Specification |
|-----------|---------------|
| **Precision** | All floating-point metrics rounded to 2 decimal places |
| **Completeness** | Output includes all 7 data points: 4 input + 3 computed |
| **Consistency** | JSON and text outputs contain identical values |
| **Format Validity** | JSON output is valid, parseable JSON; text is UTF-8 encoded |
| **Timestamp Format** | ISO 8601 format with UTC timezone (`YYYY-MM-DDTHH:MM:SSZ`) |

---

## Error Contract

**Purpose**: Define error responses for invalid input or processing failures.

### Error Response Format

```python
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error description",
        "field": "field_name (if applicable)",
        "valid_range": "description of valid values"
    }
}
```

### Error Codes & Messages

| Error Code | HTTP Status | Message | Field | Trigger | Recovery |
|------------|-------------|---------|-------|---------|----------|
| `INVALID_BALLS` | 400 | "balls must be greater than 0 to calculate strike rate" | balls | `balls = 0` | Provide balls > 0 |
| `INVALID_BOUNDARIES` | 400 | "Must have at least one boundary (four or six) to compute metrics" | fours, sixes | `(fours + sixes) = 0` | Provide fours or sixes > 0 |
| `NEGATIVE_RUNS` | 400 | "runs cannot be negative" | runs | `runs < 0` | Provide runs ≥ 0 |
| `NEGATIVE_BALLS` | 400 | "balls cannot be negative" | balls | `balls < 0` | Provide balls > 0 |
| `NEGATIVE_FOURS` | 400 | "fours cannot be negative" | fours | `fours < 0` | Provide fours ≥ 0 |
| `NEGATIVE_SIXES` | 400 | "sixes cannot be negative" | sixes | `sixes < 0` | Provide sixes ≥ 0 |
| `INVALID_TYPE` | 400 | "Expected integer for {field}, got {actual_type}" | field | Non-integer value provided | Convert to integer |
| `MISSING_FIELD` | 400 | "Required field '{field}' is missing" | field | Required field not provided | Provide the field |

### Example Error Response

```json
{
    "error": {
        "code": "INVALID_BALLS",
        "message": "balls must be greater than 0 to calculate strike rate",
        "field": "balls",
        "valid_range": "integer >= 1"
    }
}
```

---

## State Contract

**Purpose**: Define internal state visibility and state transitions.

### State Visibility (LangGraph Nodes)

| Node | State Input | State Output | Purpose |
|------|------------|--------------|---------|
| `validate_input` | raw_input | validation_result, errors | Validate input data |
| `compute_metrics` | validated_input | computed_metrics | Calculate all metrics |
| `generate_summary` | (input + metrics) | summary_output | Format output |
| `error_handler` | errors | error_response | Format errors |

### State Transition Diagram

```
START
  ↓
[validate_input]
  ├─ Valid → continue to next node
  └─ Invalid → [error_handler] → END
  ↓
[compute_metrics]
  ├─ Success → continue to next node
  └─ Failure → [error_handler] → END
  ↓
[generate_summary]
  ├─ Success → return output
  └─ Failure → [error_handler] → END
  ↓
END (with output or error)
```

---

## Library API

### Function Signatures

```python
# Main entry point
def analyze_innings(
    runs: int,
    balls: int,
    fours: int,
    sixes: int,
    output_format: Literal["json", "text"] = "json"
) -> Union[dict, str]:
    """
    Analyze batting metrics for a cricket innings.
    
    Args:
        runs: Total runs scored (must be ≥ 0)
        balls: Total balls faced (must be > 0)
        fours: Number of four-run boundary shots (must be ≥ 0)
        sixes: Number of six-run boundary shots (must be ≥ 0)
        output_format: Either "json" for structured output or "text" for formatted text
    
    Returns:
        If output_format="json": dict with complete innings data and metrics
        If output_format="text": str with formatted text summary
    
    Raises:
        ValueError: If input validation fails (negative values, zero balls, no boundaries)
        TypeError: If input types are incorrect (not integers)
    """
    pass
```

### CLI Interface

```bash
# Basic usage
python -m batting_metrics --runs 50 --balls 40 --fours 3 --sixes 1

# With format option
python -m batting_metrics --runs 50 --balls 40 --fours 3 --sixes 1 --format json
python -m batting_metrics --runs 50 --balls 40 --fours 3 --sixes 1 --format text

# Help
python -m batting_metrics --help
```

---

**Version**: 1.0.0 | **Status**: Contract Complete
