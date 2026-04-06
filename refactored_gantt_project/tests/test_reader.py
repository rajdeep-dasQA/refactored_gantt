"""Integration tests for the input reader."""
import unittest
from datetime import datetime
from pathlib import Path
import tempfile, os
from openpyxl import Workbook
from gantt.io.reader import read_project

def write_input(tmp_dir, rows, start="2025-01-06", hpd=6):
    wb=Workbook(); ws=wb.active
    ws.append(["Start Date", start])
    ws.append(["Hours Per Day", hpd])
    ws.append(["Summary","Assignee","Priority","Estimated Hours"])
    for r in rows: ws.append(r)
    path=os.path.join(tmp_dir,"input.xlsx"); wb.save(path); return path

class TestConfigParsing(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.mkdtemp()
    def test_reads_start_date(self):
        p=write_input(self.tmp,[["T1","Alice",1,4]])
        self.assertEqual(read_project(p).start_date, datetime(2025,1,6))
    def test_reads_hours_per_day(self):
        p=write_input(self.tmp,[["T1","Alice",1,4]],hpd=8)
        self.assertEqual(read_project(p).hours_per_day, 8.0)
    def test_missing_start_date_raises(self):
        wb=Workbook(); ws=wb.active
        ws.append(["Summary","Assignee","Priority","Estimated Hours"])
        ws.append(["T1","Alice",1,4])
        p=os.path.join(self.tmp,"bad.xlsx"); wb.save(p)
        with self.assertRaises(ValueError): read_project(p)

class TestTaskParsing(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.mkdtemp()
    def test_basic_task(self):
        p=write_input(self.tmp,[["Setup DB","Bob",1,10]])
        t=read_project(p).tasks[0]
        self.assertEqual(t.summary,"Setup DB"); self.assertEqual(t.assignee,"Bob")
        self.assertEqual(t.priority,1); self.assertEqual(t.hours,10.0)
    def test_sorted_by_priority(self):
        p=write_input(self.tmp,[["Low","Alice",3,4],["High","Bob",1,4]])
        tasks=read_project(p).tasks
        self.assertEqual(tasks[0].priority,1); self.assertEqual(tasks[1].priority,3)
    def test_same_priority_preserves_order(self):
        p=write_input(self.tmp,[["A","x",2,4],["B","x",2,4],["C","x",2,4]])
        names=[t.summary for t in read_project(p).tasks]
        self.assertEqual(names,["A","B","C"])
    def test_total_row_skipped(self):
        p=write_input(self.tmp,[["Real","Alice",1,6],["TOTAL HOURS",None,None,6]])
        self.assertEqual(len(read_project(p).tasks),1)
    def test_total_hours(self):
        p=write_input(self.tmp,[["T1","A",1,6],["T2","B",2,8],["T3","C",3,4]])
        self.assertAlmostEqual(read_project(p).total_hours,18.0)

if __name__ == "__main__": unittest.main()
