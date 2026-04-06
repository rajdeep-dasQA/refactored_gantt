from pathlib import Path
from gantt.io.reader import read_project
from gantt.renderer.workbook_builder import generate_gantt_workbook
from gantt.scheduler.engine import schedule

def process_file(input_path: str, output_path: str):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    project = read_project(input_path)
    schedule(project.tasks, project.start_date, project.hours_per_day)
    generate_gantt_workbook(project, str(output_path))

    return output_path
