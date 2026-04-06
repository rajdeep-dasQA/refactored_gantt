#!/usr/bin/env python3
"""
Gantt Chart Generator — CLI entry point.

Default behaviour (no arguments):
    Reads from:  target_estimations/sample_input.xlsx
    Writes to:   generated_charts/gantt_chart.xlsx

Usage
-----
    python main.py                              # use default paths above
    python main.py path/to/input.xlsx           # custom input, default output folder
    python main.py input.xlsx output.xlsx       # fully custom paths
    python main.py --template [path]            # (re)generate the input template
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from gantt.io.reader import read_project
from gantt.renderer.workbook_builder import generate_gantt_workbook, generate_input_template
from gantt.scheduler.engine import schedule

# ---------------------------------------------------------------------------
# Project-level default paths
# ---------------------------------------------------------------------------
ROOT             = Path(__file__).parent
DEFAULT_INPUT    = ROOT / "target_estimations" / "sample_input.xlsx"
OUTPUT_DIR       = ROOT / "generated_charts"
DEFAULT_OUTPUT   = OUTPUT_DIR / "gantt_chart.xlsx"
TEMPLATE_PATH    = ROOT / "target_estimations" / "sample_input.xlsx"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gantt",
        description=(
            "Generate an Excel Gantt chart (daily + weekly views) from an input sheet.\n"
            f"Default input  : {DEFAULT_INPUT}\n"
            f"Default output : {DEFAULT_OUTPUT}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--template",
        nargs="?",
        const=str(TEMPLATE_PATH),
        metavar="PATH",
        help=(
            f"Regenerate the input template (default: {TEMPLATE_PATH}). "
            "Pass a custom path to write it elsewhere."
        ),
    )

    parser.add_argument(
        "input",
        nargs="?",
        default=str(DEFAULT_INPUT),
        metavar="INPUT",
        help=f"Path to a filled input .xlsx (default: {DEFAULT_INPUT}).",
    )

    parser.add_argument(
        "output",
        nargs="?",
        default=str(DEFAULT_OUTPUT),
        metavar="OUTPUT",
        help=f"Destination for the generated Gantt .xlsx (default: {DEFAULT_OUTPUT}).",
    )

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = build_parser()
    args   = parser.parse_args()

    # ── Template (re)generation ───────────────────────────────────────────
    if args.template is not None:
        out = Path(args.template)
        out.parent.mkdir(parents=True, exist_ok=True)
        print(f"Generating input template → {out}")
        generate_input_template(str(out))
        print(f"✅  Template saved: {out}")
        return 0

    # ── Gantt generation ──────────────────────────────────────────────────
    input_path  = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"❌  Input file not found: {input_path}", file=sys.stderr)
        print(f"   Run  python main.py --template  to regenerate the sample input.", file=sys.stderr)
        return 1

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading input   → {input_path}")
    project = read_project(input_path)

    print(
        f"Scheduling {len(project.tasks)} tasks "
        f"({project.total_hours:.0f}h @ {project.hours_per_day}h/day) …"
    )
    schedule(project.tasks, project.start_date, project.hours_per_day)

    print(
        f"  Project span   : "
        f"{project.start_date.strftime('%d %b %Y')} – "
        f"{project.project_end.strftime('%d %b %Y')}"
    )

    print(f"Generating Gantt → {output_path}")
    generate_gantt_workbook(project, str(output_path))

    print(f"✅  Done! Open {output_path} and click the sheet tabs to switch views.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
