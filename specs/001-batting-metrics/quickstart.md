# Quick Start Guide: Batting Metrics Analysis

**Date**: 2026-03-02 | **Plan**: [plan.md](plan.md) | **Data Model**: [data-model.md](data-model.md)

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/[org]/scoreSummary.git
cd scoreSummary

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

### Requirements

- Python 3.11 or higher
- Dependencies (automatically installed):
  - LangGraph 0.1.0+
  - Pydantic 2.0+
  - Python standard library only for CLI

## Basic Usage

### As a Python Library

```python
from batting_metrics import analyze_innings

# Example 1: Basic usage (returns JSON by default)
result = analyze_innings(
    runs=50,
    balls=40,
    fours=3,
    sixes=1
)
print(result)

# Output (formatted):
# {
#   "input": {"runs": 50, "balls": 40, "fours": 3, "sixes": 1},
#   "metrics": {"strike_rate": 125.0, "boundary_percentage": 36.0, "balls_per_boundary": 10.0}
# }
```

### Text Format Output

```python
from batting_metrics import analyze_innings

summary = analyze_innings(
    runs=75,
    balls=60,
    fours=4,
    sixes=2,
    output_format="text"
)
print(summary)

# Example output (truncated):
# ═══════════════════════════════════════════════════════
#        BATTING METRICS SUMMARY
# ═══════════════════════════════════════════════════════
#
# INPUT STATISTICS
# ──────────────────────────────────────────────────────
#   Runs Scored:               75
#   Balls Faced:               60
#   Four-Run Boundaries:       4
#   Six-Run Boundaries:        2
#
# COMPUTED METRICS
# ──────────────────────────────────────────────────────
#   Strike Rate:              125.00 (runs per 100 balls)
#   Boundary Percentage:       26.67%
#   Balls Per Boundary:        10.00
# ═══════════════════════════════════════════════════════
```
### Command-Line Interface (CLI)

```bash
# Basic analysis with JSON output (default)
python -m batting_metrics --runs 50 --balls 40 --fours 3 --sixes 1

# Output: JSON formatted result

# Text format output
python -m batting_metrics --runs 50 --balls 40 --fours 3 --sixes 1 --format text

# Output: Formatted text summary

# Help
python -m batting_metrics --help
```

## Common Use Cases

### Use Case 1: Analyze a Single Innings (MVP)

**Scenario**: Cricket analyst needs quick metrics for an innings just completed.

```python
from batting_metrics import analyze_innings

# Batsman scored 87 runs in 72 balls with 8 fours and 2 sixes
result = analyze_innings(runs=87, balls=72, fours=8, sixes=2)

# Extract specific metrics
strike_rate = result["innings"]["metrics"]["strike_rate"]
print(f"Strike Rate: {strike_rate} runs per 100 balls")
# Output: Strike Rate: 120.83 runs per 100 balls
```

### Use Case 2: Batch Analysis from Data

**Scenario**: Analyze multiple innings in sequence.

```python
from batting_metrics import analyze_innings

innings_data = [
    {"runs": 50, "balls": 40, "fours": 3, "sixes": 1},
    {"runs": 75, "balls": 60, "fours": 4, "sixes": 2},
    {"runs": 65, "balls": 55, "fours": 5, "sixes": 1},
]

for i, innings in enumerate(innings_data, 1):
    try:
        result = analyze_innings(**innings, output_format="text")
        print(f"\n--- Innings {i} ---")
        print(result)
    except ValueError as e:
        print(f"Innings {i} error: {e}")
```

### Use Case 3: Generate Report with Text Output

**Scenario**: Create formatted report of innings performance.

```python
from batting_metrics import analyze_innings

# Get formatted text for reporting/printing
report = analyze_innings(
    runs=92,
    balls=70,
    fours=10,
    sixes=3,
    output_format="text"
)

# Write to file
with open("innings_report.txt", "w") as f:
    f.write(report)
```

### Use Case 4: Error Handling

**Scenario**: Gracefully handle invalid input.

```python
from batting_metrics import analyze_innings

test_cases = [
    (50, 40, 3, 1),      # Valid
    (50, 0, 3, 1),       # Invalid: balls = 0
    (50, 40, 0, 0),      # Invalid: no boundaries
    (-10, 40, 3, 1),     # Invalid: negative runs
]

for runs, balls, fours, sixes in test_cases:
    try:
        result = analyze_innings(runs=runs, balls=balls, fours=fours, sixes=sixes)
        print(f"✓ Valid: {runs} runs, {balls} balls, {fours+sixes} boundaries")
    except ValueError as e:
        print(f"✗ Error: {e}")
```

## Data Model Overview

### Input Variables

| Variable | Type | Constraint | Example |
|----------|------|-----------|---------|
| runs | int | ≥ 0 | 50 |
| balls | int | > 0 | 40 |
| fours | int | ≥ 0 | 3 |
| sixes | int | ≥ 0 | 1 |

### Computed Metrics

| Metric | Formula | Example Value |
|--------|---------|----------------|
| strike_rate | (runs ÷ balls) × 100 | 125.0 |
| boundary_percentage | ((fours×4+sixes×6) ÷ runs) × 100 | 20.0 |
| balls_per_boundary | balls ÷ (fours+sixes) | 10.0 |

## Validation Rules

The system validates input before processing:

❌ **Rejected**:
- `balls = 0` (prevents division by zero)
- `fours + sixes = 0` (prevents undefined calculation)
- Negative values for any field

✓ **Accepted**:
- `runs = 0` (valid: batsman didn't score)
- `fours = 0` and `sixes > 0` (valid: only sixes)
- `fours > 0` and `sixes = 0` (valid: only fours)

## Architecture Overview

```
User Input
    ↓
[Validation Layer] → Check constraints, reject invalid data
    ↓
[Computation Layer] → Calculate metrics using formulas
    ↓
[Output Layer] → Format as JSON or Text
    ↓
Output (JSON or Text)
```

### Technology Stack

- **State Management**: LangGraph (workflow orchestration)
- **Data Validation**: Pydantic (runtime type checking)
- **Language**: Python 3.11+
- **Output Formats**: JSON (native), Text (formatted)

## API Reference

### Main Function

```python
def analyze_innings(
    runs: int,
    balls: int,
    fours: int,
    sixes: int,
    output_format: Literal["json", "text"] = "json"
) -> Union[dict, str]:
    """
    Analyze batting metrics for a cricket innings.
    
    Validates input data, computes metrics (strike rate, boundary 
    percentage, balls per boundary), and returns results in requested format.
    
    Args:
        runs: Total runs scored (non-negative integer)
        balls: Total balls faced (positive integer, must be > 0)
        fours: Number of four-run boundary shots (non-negative integer)
        sixes: Number of six-run boundary shots (non-negative integer)
        output_format: Format for output - "json" or "text" (default: "json")
    
    Returns:
        dict: If output_format="json", returns structured data with input
              and computed metrics
        str: If output_format="text", returns formatted text summary
    
    Raises:
        ValueError: If input validation fails (specific error message indicates issue)
        TypeError: If input data types are incorrect
    
    Examples:
        # JSON output (default)
        result = analyze_innings(runs=50, balls=40, fours=3, sixes=1)
        
        # Text output
        summary = analyze_innings(runs=50, balls=40, fours=3, sixes=1, 
                                  output_format="text")
    """
    pass
```

## Troubleshooting

### Issue: "balls must be greater than 0"
**Cause**: Input has `balls=0`  
**Solution**: Provide a valid number of balls (e.g., `balls=40`)

### Issue: "Must have at least one boundary"
**Cause**: Input has `fours=0` and `sixes=0`  
**Solution**: Set at least one boundary (e.g., `fours=1` or `sixes=1`)

### Issue: Negative values rejected
**Cause**: Input has negative `runs`, `balls`, `fours`, or `sixes`  
**Solution**: Use only non-negative values (≥ 0 for runs/fours/sixes, > 0 for balls)

### Issue: Import error when using library
**Cause**: Package not installed  
**Solution**: Run `pip install -e .` from project root

## Next Steps

1. **For Library Usage**: Import and use in your Python applications
2. **For CLI Usage**: Run Python module directly
3. **For Development**: See [plan.md](plan.md) for implementation details
4. **For Specification**: See [spec.md](../spec.md) for requirements

---

**Version**: 1.0.0 | **Status**: Guide Complete | **Last Updated**: 2026-03-02
