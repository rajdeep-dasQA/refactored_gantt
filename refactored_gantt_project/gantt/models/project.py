"""
Aggregate model that holds project-level configuration and the task list.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

from gantt.models.task import Task


@dataclass
class Project:
    start_date:    datetime
    hours_per_day: float
    tasks:         list[Task] = field(default_factory=list)

    # ------------------------------------------------------------------
    @property
    def project_end(self) -> datetime:
        if not self.tasks:
            raise ValueError("No tasks scheduled yet.")
        scheduled = [t for t in self.tasks if t.is_scheduled()]
        if not scheduled:
            raise ValueError("Tasks have not been scheduled yet.")
        return max(t.end_date for t in scheduled)  # type: ignore[return-value]

    @property
    def total_hours(self) -> float:
        return sum(t.hours for t in self.tasks)

    def __repr__(self) -> str:
        return (
            f"Project(start={self.start_date.strftime('%d %b %Y')}, "
            f"{self.hours_per_day}h/day, {len(self.tasks)} tasks, "
            f"{self.total_hours:.0f}h total)"
        )
