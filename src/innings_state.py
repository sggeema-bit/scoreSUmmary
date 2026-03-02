"""State models for batting metrics analysis."""

from pydantic import BaseModel, Field, validator
from typing import Optional


class InningsInput(BaseModel):
    """User-provided innings data."""

    runs: int = Field(ge=0, description="Total runs scored in the innings")
    balls: int = Field(gt=0, description="Total balls faced (must be > 0)")
    fours: int = Field(ge=0, description="Number of four-run boundaries")
    sixes: int = Field(ge=0, description="Number of six-run boundaries")

    @validator("balls")
    def validate_balls_not_zero(cls, v):
        if v == 0:
            raise ValueError("balls must be greater than 0 to calculate strike rate")
        return v

    @validator("fours", "sixes", always=True)
    def validate_boundaries_sum(cls, v, values):
        fours_val = values.get("fours", 0)
        sixes_val = values.get("sixes", 0)
        if fours_val + sixes_val == 0:
            raise ValueError(
                "Must have at least one boundary (four or six) to compute metrics"
            )
        return v


class InningsMetrics(BaseModel):
    """Computed metrics from innings input."""

    strike_rate: float
    boundary_percentage: float
    balls_per_boundary: float


class InningsState(BaseModel):
    """Complete innings state including input and computed metrics."""

    input: InningsInput
    metrics: Optional[InningsMetrics] = None

    @classmethod
    def create_and_compute(cls, runs: int, balls: int, fours: int, sixes: int) -> "InningsState":
        """Validate inputs and compute metrics. Placeholder until computation logic added."""
        input_data = InningsInput(runs=runs, balls=balls, fours=fours, sixes=sixes)
        # metrics will be added later
        return cls(input=input_data)
