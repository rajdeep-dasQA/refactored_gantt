"""
Domain model for a single task / work item.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents one row from the input sheet."""

    summary:  str
    assignee: str
    priority: int
    hours:    float

    # Set by the scheduler — not present in raw input
    start_date:        datetime | None = field(default=None, repr=False)
    start_hour_offset: float           = field(default=0.0,  repr=False)
    end_date:          datetime | None = field(default=None, repr=False)
    end_hour_offset:   float           = field(default=0.0,  repr=False)

    # Internal: original row order for stable sort within same priority
    _order: int = field(default=0, repr=False, compare=False)

    # ------------------------------------------------------------------
    def is_scheduled(self) -> bool:
        return self.start_date is not None and self.end_date is not None

    def __repr__(self) -> str:
        scheduled = ""
        if self.is_scheduled():
            scheduled = (
                f", {self.start_date.strftime('%d %b')}–"  # type: ignore[union-attr]
                f"{self.end_date.strftime('%d %b')}"       # type: ignore[union-attr]
            )
        return f"Task({self.summary!r}, pri={self.priority}, {self.hours}h{scheduled})"
