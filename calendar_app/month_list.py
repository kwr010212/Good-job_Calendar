# calendar_app/month_list.py
import tkinter as tk
from tkinter import ttk
import datetime as dt

from .config import BASE_FONT_FAMILY, CATEGORY_DEFS
from .db import EventRepository


class MonthListWindow(tk.Toplevel):
    """
    현재 월의 모든 일정을 리스트로 보여주는 창.
    더블클릭하면 해당 날짜 DayWindow를 연다.
    """

    def __init__(
        self,
        master: tk.Tk,
        repo: EventRepository,
        year: int,
        month: int,
        open_day_window,  # (date_obj, date_str) -> None
    ):
        super().__init__(master)
        self.repo = repo
        self.year = year
        self.month = month
        self.open_day_window = open_day_window

        self.title(f"{year}년 {month}월 전체 일정")
        self.geometry("560x450")
        self.configure(bg="#f9fafb")
        self.configure(highlightbackground="#cbd5f5", highlightthickness=1)

        tk.Label(
            self,
            text=f"{year}년 {month}월 일정 목록",
            bg="#f9fafb",
            fg="#0f172a",
            font=(BASE_FONT_FAMILY, 12, "bold"),
        ).pack(anchor="w", padx=12, pady=(10, 4))

        frame = tk.Frame(self, bg="#f9fafb")
        frame.pack(fill="both", expand=True, padx=12, pady=(4, 8))

        columns = ("date", "time", "title", "category")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.heading("date", text="날짜")
        self.tree.heading("time", text="시간")
        self.tree.heading("title", text="제목")
        self.tree.heading("category", text="구분")

        self.tree.column("date", width=90, anchor="center")
        self.tree.column("time", width=90, anchor="center")
        self.tree.column("title", width=260, anchor="w")
        self.tree.column("category", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self._load_data()

        self.tree.bind("<Double-1>", self._on_row_double_click)

    def _load_data(self):
        rows = self.repo.get_month_events(self.year, self.month)

        for r in rows:
            date_str = r["date"]
            st = r["start_time"] or ""
            et = r["end_time"] or ""
            if st and et:
                time_disp = f"{st}~{et}"
            elif st:
                time_disp = st
            elif et:
                time_disp = f"~{et}"
            else:
                time_disp = ""
            cat_key = r["category"] or "general"
            cat_label = CATEGORY_DEFS.get(
                cat_key, CATEGORY_DEFS["general"]
            )["label"]
            self.tree.insert(
                "", "end", values=(date_str, time_disp, r["title"], cat_label)
            )

    def _on_row_double_click(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        date_str = vals[0]
        try:
            y, m, d = map(int, date_str.split("-"))
            date_obj = dt.date(y, m, d)
        except ValueError:
            return

        if self.open_day_window:
            self.open_day_window(date_obj, date_str)
            self.lift()
