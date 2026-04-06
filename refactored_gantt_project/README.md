# Gantt Chart Generator

Generates a polished Excel Gantt chart from a simple input spreadsheet.
Both **Daily** and **Weekly** views are produced automatically — switch between them via the sheet tabs.

---

## Project Structure

```
gantt_project/
├── main.py                      # CLI entry point
├── requirements.txt
├── README.md
│
├── gantt/                       # Core package
│   ├── config/
│   │   └── constants.py         # Colours, palette, layout defaults
│   │
│   ├── models/
│   │   ├── task.py              # Task dataclass
│   │   └── project.py           # Project dataclass (config + task list)
│   │
│   ├── scheduler/
│   │   ├── engine.py            # Sequential scheduling + period-coverage calc
│   │   └── calendar_utils.py    # Workday helpers, period-list builders
│   │
│   ├── renderer/
│   │   ├── styles.py            # openpyxl style factories (fonts, fills, borders)
│   │   ├── sheet_builder.py     # Builds one Gantt worksheet (day or week)
│   │   └── workbook_builder.py  # Orchestrates both sheets + template writer
│   │
│   └── io/
│       └── reader.py            # Reads input .xlsx → Project instance
│
└── tests/
    ├── test_scheduler.py        # Unit tests: scheduling + calendar utils
    └── test_reader.py           # Integration tests: input parsing
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Generate a blank input template

```bash
python main.py --template
# → gantt_input_template.xlsx

python main.py --template my_project.xlsx
# → my_project.xlsx
```

### 2. Fill in the template

Open `gantt_input_template.xlsx` and fill in:

| Field | Description |
|---|---|
| **Start Date** | Project start date (`YYYY-MM-DD`) |
| **Hours Per Day** | Productive working hours per day |
| **Summary** | Task name |
| **Assignee** | Person responsible |
| **Priority** | Integer (1 = highest). Tasks are sorted by priority, then by row order within the same priority. |
| **Estimated Hours** | Total hours estimated for the task |

### 3. Generate the Gantt chart

```bash
python main.py my_project.xlsx
# → gantt_chart.xlsx

python main.py my_project.xlsx reports/sprint1_gantt.xlsx
# → reports/sprint1_gantt.xlsx
```

---

## Output

The generated `.xlsx` contains two sheet tabs:

| Tab | Description |
|---|---|
| 📅 **Daily View** | One column per working day. Cell value = hours worked that day. |
| 📆 **Weekly View** | One column per calendar week. Cell value = hours worked that week. |

**Color coding** is based on priority level:

| Priority | Color |
|---|---|
| 1 | 🟩 Green |
| 2 | 🟦 Blue |
| 3 | 🟧 Orange |
| 4 | 🟨 Yellow |
| 5 | 🫒 Olive Green |

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```
