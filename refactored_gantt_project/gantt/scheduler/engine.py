"""
Scheduling engine.

Responsibilities
----------------
* Assign start/end dates + fractional-hour offsets to every Task (mutates in place).
* Calculate hours a task contributes within any arbitrary date range (period coverage).
"""
from __future__ import annotations
from datetime import datetime, timedelta

from gantt.config.constants import WORK_DAYS
from gantt.models.task import Task
from gantt.scheduler.calendar_utils import next_workday


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

def schedule(tasks: list[Task], start_date: datetime, hours_per_day: float) -> None:
    """
    Sequentially assign start/end dates to each task, respecting workdays and
    the fractional hours remaining on a shared day.

    Mutates each Task in *tasks* in-place, setting:
        - start_date        – calendar day the task begins
        - start_hour_offset – hours already consumed on that day before this task
        - end_date          – calendar day the task finishes
        - end_hour_offset   – hours consumed on end_date after this task completes
    """
    current = _first_workday(start_date)
    used    = 0.0  # hours consumed on *current* so far

    for task in tasks:
        task.start_date        = current
        task.start_hour_offset = used

        remaining = task.hours
        while remaining > 0:
            available = hours_per_day - used
            if available <= 0:
                current   = next_workday(current)
                used      = 0.0
                available = hours_per_day

            taken      = min(available, remaining)
            remaining -= taken
            used      += taken

            if remaining > 0 and used >= hours_per_day:
                current = next_workday(current)
                used    = 0.0

        task.end_date        = current
        task.end_hour_offset = used

        # If the day is fully consumed, advance so the next task starts fresh
        if used >= hours_per_day:
            current = next_workday(current)
            used    = 0.0


def _first_workday(dt: datetime) -> datetime:
    while dt.weekday() not in WORK_DAYS:
        dt += timedelta(days=1)
    return dt


# ---------------------------------------------------------------------------
# Period coverage
# ---------------------------------------------------------------------------

def hours_in_period(
    task: Task,
    period_start: datetime,
    period_end:   datetime,
    hours_per_day: float,
) -> float:
    """
    Return the number of hours *task* contributes within [period_start, period_end].

    Handles:
    * Tasks that start and end on the same day (fractional single-day task).
    * Partial first day  (start_hour_offset > 0).
    * Partial last day   (end_hour_offset   < hours_per_day).
    * Full middle days.
    """
    ts, te = task.start_date, task.end_date
    if te < period_start or ts > period_end:  # type: ignore[operator]
        return 0.0

    hours = 0.0
    day   = max(ts, period_start)   # type: ignore[type-var]
    end   = min(te, period_end)     # type: ignore[type-var]

    while day <= end:
        if day.weekday() in WORK_DAYS:
            if ts == te:
                # Single-day task — total hours fit inside one day
                hours += task.hours
            elif day == ts:
                hours += hours_per_day - task.start_hour_offset
            elif day == te:
                hours += task.end_hour_offset
            else:
                hours += hours_per_day
        day += timedelta(days=1)

    return round(min(hours, task.hours), 1)
