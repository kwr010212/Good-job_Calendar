# calendar_app/search_window.py
import tkinter as tk
from tkinter import ttk
import datetime as dt

from .config import BASE_FONT_FAMILY, CATEGORY_DEFS
from .db import EventRepository


class SearchWindow(tk.Toplevel):
    """
    일정 검색 창.
    - 키워드
    - 카테고리 필터
    """

    def __init__(
        self,
        master: tk.Tk,
        repo: EventRepository,
        open_day_window,  # (date_obj, date_str) -> None
    ):
        super().__init__(master)
        self.repo = repo
        self.open_day_window = open_day_window

        self.title("일정 검색")
        self.geometry("540x430")
        self.configure(bg="#f9fafb")
        self.configure(highlightbackground="#cbd5f5", highlightthickness=1)

        tk.Label(
            self,
            text="검색어 (제목/메모 포함)",
            bg="#f9fafb",
            fg="#0f172a",
            font=(BASE_FONT_FAMILY, 10),
        ).pack(anchor="w", padx=12, pady=(10, 0))

        self.kw_var = tk.StringVar()
        kw_entry = ttk.Entry(self, textvariable=self.kw_var,
                             font=(BASE_FONT_FAMILY, 10))
        kw_entry.pack(fill="x", padx=12, pady=(4, 6))

        tk.Label(
            self,
            text="구분 필터 (선택사항)",
            bg="#f9fafb",
            fg="#0f172a",
            font=(BASE_FONT_FAMILY, 10),
        ).pack(anchor="w", padx=12, pady=(2, 0))

        cat_frame = tk.Frame(self, bg="#f9fafb")
        cat_frame.pack(fill="x", padx=12, pady=(2, 6))

        self.search_cat_var = tk.StringVar(value="전체")
        cat_values = ["전체"] + [info["label"] for info in CATEGORY_DEFS.values()]
        self.cat_combo = ttk.Combobox(
            cat_frame,
            textvariable=self.search_cat_var,
            values=cat_values,
            state="readonly",
            width=10,
        )
        self.cat_combo.pack(side="left")

        self.label_to_key = {CATEGORY_DEFS[k]["label"]: k for k in CATEGORY_DEFS}

        result_frame = tk.Frame(self, bg="#f9fafb")
        result_frame.pack(fill="both", expand=True, padx=12, pady=(4, 8))

        columns = ("date", "time", "title", "category")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        self.tree.heading("date", text="날짜")
        self.tree.heading("time", text="시간")
        self.tree.heading("title", text="제목")
        self.tree.heading("category", text="구분")

        self.tree.column("date", width=90, anchor="center")
        self.tree.column("time", width=90, anchor="center")
        self.tree.column("title", width=260, anchor="w")
        self.tree.column("category", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

        search_btn = ttk.Button(
            self, text="검색", command=self._do_search, style="Main.TButton"
        )
        search_btn.pack(pady=(0, 4))

        self.tree.bind("<Double-1>", self._on_row_double_click)
        kw_entry.focus_set()

    def _do_search(self):
        keyword = self.kw_var.get().strip()
        cat_label = self.search_cat_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        cat_key = None
        if cat_label != "전체":
            cat_key = self.label_to_key.get(cat_label)

        rows = self.repo.search_events(keyword or None, cat_key)

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
            cat_label_disp = CATEGORY_DEFS.get(
                cat_key, CATEGORY_DEFS["general"]
            )["label"]

            self.tree.insert(
                "", "end",
                values=(date_str, time_disp, r["title"], cat_label_disp)
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
