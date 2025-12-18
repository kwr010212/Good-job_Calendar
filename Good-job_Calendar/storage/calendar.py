# pages/calendar.py
import tkinter as tk
from tkinter import ttk
import core

class CalendarPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        header = ttk.Frame(self)
        header.pack(fill="x", pady=6)
        ttk.Label(header, text="달력", font=("Arial", 16)).pack(side="left", padx=6)

        btns = ttk.Frame(header); btns.pack(side="right")
        self.year_var = tk.IntVar(value=int(core.today_str().split("-")[0]))
        self.month_var = tk.IntVar(value=int(core.today_str().split("-")[1]))

        ttk.Button(btns, text="◀", command=self.prev_month).pack(side="left")
        ttk.Button(btns, text="▶", command=self.next_month).pack(side="left")
        ttk.Button(btns, text="홈", command=lambda: controller.show("Home")).pack(side="left", padx=6)

        self.canvas = ttk.Frame(self)
        self.canvas.pack(fill="both", expand=True)
        self.draw_calendar()

    def prev_month(self):
        y = self.year_var.get(); m = self.month_var.get()
        m -= 1
        if m < 1:
            m = 12; y -= 1
        self.year_var.set(y); self.month_var.set(m); self.draw_calendar()

    def next_month(self):
        y = self.year_var.get(); m = self.month_var.get()
        m += 1
        if m > 12:
            m = 1; y += 1
        self.year_var.set(y); self.month_var.set(m); self.draw_calendar()

    def draw_calendar(self):
        for w in self.canvas.winfo_children():
            w.destroy()
        y = self.year_var.get(); m = self.month_var.get()
        weeks = core.get_month_matrix(y, m)
        days = ["일","월","화","수","목","금","토"]
        hdr = ttk.Frame(self.canvas); hdr.pack(fill="x")
        for d in days:
            ttk.Label(hdr, text=d, width=12, anchor="center").pack(side="left")
        for week in weeks:
            row = ttk.Frame(self.canvas); row.pack(fill="x", expand=True)
            for cell in week:
                frame = ttk.Frame(row, relief="ridge", borderwidth=1)
                frame.pack(side="left", fill="both", expand=True)
                ttk.Label(frame, text=str(cell['day']) if cell['day'] else "").pack(anchor="nw")
                if cell['date_str']:
                    items = [it for it in core.get_all_schedules() if it.get("date")==cell['date_str']]
                    for it in items[:3]:
                        ttk.Label(frame, text=f"- {it['title']}", anchor="w").pack(anchor="w")
