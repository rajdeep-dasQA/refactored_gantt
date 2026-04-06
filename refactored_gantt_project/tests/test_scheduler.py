"""Unit tests for scheduler engine and calendar utilities."""
import unittest
from datetime import datetime

from gantt.models.task import Task
from gantt.scheduler.engine import schedule, hours_in_period
from gantt.scheduler.calendar_utils import next_workday, week_monday, build_day_periods, build_week_periods

MON=datetime(2025,1,6); TUE=datetime(2025,1,7); WED=datetime(2025,1,8)
THU=datetime(2025,1,9); FRI=datetime(2025,1,10); SAT=datetime(2025,1,11)
SUN=datetime(2025,1,12); NEXT_MON=datetime(2025,1,13)

def make_task(summary="Task", priority=1, hours=6.0, order=0):
    return Task(summary=summary, assignee="Alice", priority=priority, hours=hours, _order=order)

def scheduled(start, s_off, end, e_off, hours):
    t=make_task(hours=hours); t.start_date=start; t.start_hour_offset=s_off
    t.end_date=end; t.end_hour_offset=e_off; return t

class TestNextWorkday(unittest.TestCase):
    def test_friday_to_monday(self): self.assertEqual(next_workday(FRI), NEXT_MON)
    def test_saturday_to_monday(self): self.assertEqual(next_workday(SAT), NEXT_MON)
    def test_sunday_to_monday(self): self.assertEqual(next_workday(SUN), NEXT_MON)
    def test_monday_to_tuesday(self): self.assertEqual(next_workday(MON), TUE)

class TestWeekMonday(unittest.TestCase):
    def test_monday_unchanged(self): self.assertEqual(week_monday(MON), MON)
    def test_friday_returns_monday(self): self.assertEqual(week_monday(FRI), MON)
    def test_sunday_returns_monday(self): self.assertEqual(week_monday(SUN), MON)

class TestBuildPeriods(unittest.TestCase):
    def test_day_periods_mon_to_fri(self): self.assertEqual(len(build_day_periods(MON, FRI)), 5)
    def test_day_periods_skip_weekend(self): self.assertEqual(len(build_day_periods(MON, NEXT_MON)), 6)
    def test_week_periods_single_week(self): self.assertEqual(len(build_week_periods(MON, FRI)), 2)
    def test_week_period_label(self): self.assertTrue(build_week_periods(MON,FRI)[0][0].startswith("Wk1"))

class TestSchedule(unittest.TestCase):
    def test_single_task_fits_one_day(self):
        t=make_task(hours=6.0); schedule([t], MON, 6)
        self.assertEqual(t.start_date, MON); self.assertEqual(t.end_date, MON)

    def test_single_task_spans_two_days(self):
        t=make_task(hours=8.0); schedule([t], MON, 6)
        self.assertEqual(t.start_date, MON); self.assertEqual(t.end_date, TUE)

    def test_two_tasks_share_a_day(self):
        t1=make_task("T1",hours=4.0,order=0); t2=make_task("T2",hours=4.0,order=1)
        schedule([t1,t2], MON, 6)
        self.assertEqual(t1.start_date, MON); self.assertEqual(t2.start_date, MON)
        self.assertAlmostEqual(t1.end_hour_offset, 4.0)
        self.assertAlmostEqual(t2.start_hour_offset, 4.0)

    def test_full_day_pushes_next_task(self):
        t1=make_task("T1",hours=6.0,order=0); t2=make_task("T2",hours=6.0,order=1)
        schedule([t1,t2], MON, 6)
        self.assertEqual(t1.end_date, MON); self.assertEqual(t2.start_date, TUE)

    def test_weekend_start_advances_to_monday(self):
        t=make_task(hours=6.0); schedule([t], SAT, 6)
        self.assertEqual(t.start_date, NEXT_MON)

    def test_priority_order_respected(self):
        t_low=make_task("Low",priority=3,hours=6.0,order=0); t_high=make_task("High",priority=1,hours=6.0,order=1)
        tasks=sorted([t_low,t_high],key=lambda x:(x.priority,x._order))
        schedule(tasks, MON, 6)
        self.assertEqual(tasks[0].summary,"High"); self.assertEqual(tasks[0].start_date, MON)
        self.assertEqual(tasks[1].summary,"Low"); self.assertEqual(tasks[1].start_date, TUE)

class TestHoursInPeriod(unittest.TestCase):
    def test_no_overlap_before(self): self.assertEqual(hours_in_period(scheduled(WED,0,WED,6,6), MON, TUE, 6), 0.0)
    def test_no_overlap_after(self): self.assertEqual(hours_in_period(scheduled(MON,0,MON,6,6), WED, THU, 6), 0.0)
    def test_single_full_day(self): self.assertAlmostEqual(hours_in_period(scheduled(MON,0,MON,6,6), MON, MON, 6), 6.0)
    def test_partial_start_day(self): self.assertAlmostEqual(hours_in_period(scheduled(MON,4,TUE,2,4), MON, MON, 6), 2.0)
    def test_partial_end_day(self): self.assertAlmostEqual(hours_in_period(scheduled(MON,0,TUE,3,9), TUE, TUE, 6), 3.0)
    def test_multi_day_full_coverage(self): self.assertAlmostEqual(hours_in_period(scheduled(MON,0,WED,6,18), MON, WED, 6), 18.0)
    def test_capped_at_task_hours(self): self.assertAlmostEqual(hours_in_period(scheduled(MON,0,MON,4,4), MON, FRI, 6), 4.0)

if __name__ == "__main__": unittest.main()
