"""Command-line interface for batting metrics."""

import argparse
from .main import analyze_innings


def main():
    parser = argparse.ArgumentParser(description="Analyze batting metrics for a cricket innings")
    parser.add_argument("--runs", type=int, required=True, help="Total runs scored")
    parser.add_argument("--balls", type=int, required=True, help="Total balls faced")
    parser.add_argument("--fours", type=int, required=True, help="Number of four-run boundaries")
    parser.add_argument("--sixes", type=int, required=True, help="Number of six-run boundaries")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")

    args = parser.parse_args()
    result = analyze_innings(
        runs=args.runs,
        balls=args.balls,
        fours=args.fours,
        sixes=args.sixes,
        output_format=args.format,
    )
    print(result)
