"""
Calendar utilities: workday arithmetic and period generation.
"""
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Literal

from gantt.config.constants import WORK_DAYS


def next_workday(dt: datetime) -> datetime:
    """Return the first workday strictly after *dt*."""
    dt += timedelta(days=1)
    while dt.weekday() not in WORK_DAYS:
        dt += timedelta(days=1)
    return dt


def week_monday(dt: datetime) -> datetime:
    """Return the Monday of the week containing *dt*."""
    return dt - timedelta(days=dt.weekday())


# ---------------------------------------------------------------------------
# Period generation
# ---------------------------------------------------------------------------
Period = tuple[str, datetime, datetime]   # (label, period_start, period_end)

def _fmt_day(dt: datetime) -> str:
    return f"{dt.day} {dt.strftime('%b')}"

def build_day_periods(start: datetime, end: datetime) -> list[Period]:
    """One period per workday from *start* to *end* inclusive."""
    periods: list[Period] = []
    day = start
    n   = 1
    while day <= end:
        if day.weekday() in WORK_DAYS:
            periods.append((f"Day{n}\n{_fmt_day(day)}", day, day))
            n += 1
        day += timedelta(days=1)
    return periods


def build_week_periods(start: datetime, end: datetime) -> list[Period]:
    """One period per calendar week (Mon–Sun) covering *start* to *end*."""
    periods: list[Period] = []
    wk = week_monday(start)
    n  = 1
    while wk <= end + timedelta(days=6):
        label = f"Wk{n}\n{_fmt_day(wk)}"
        periods.append((label, wk, wk + timedelta(days=6)))
        wk += timedelta(days=7)
        n  += 1
    return periods


def get_periods(
    start: datetime,
    end: datetime,
    mode: Literal["day", "week"],
) -> list[Period]:
    """Dispatch to the correct period builder based on *mode*."""
    if mode == "week":
        return build_week_periods(start, end)
    return build_day_periods(start, end)
