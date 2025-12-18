# pages/timetable.py
import tkinter as tk
from tkinter import ttk
import core

class TimetablePage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        ttk.Label(self, text="시간표", font=("Arial", 16)).pack(pady=8)

        # 상단 고정 영역 (삭제되면 안 됨!)
        self.top = ttk.Frame(self)
        self.top.pack(fill="x", padx=8)
        ttk.Button(self.top, text="홈", 
                   command=lambda: controller.show("Home")).pack(side="right")

        # 버튼 고정 영역
        self.btns = ttk.Frame(self)
        self.btns.pack(pady=6)
        ttk.Button(self.btns, text="샘플 추가(mon 수업)", 
                   command=self.add_sample).pack()

        # 시간표가 들어갈 영역
        self.content = ttk.Frame(self)
        self.content.pack(fill="both", expand=True, padx=8, pady=6)

        self.render()

    def add_sample(self):
        core.add_class("mon", "09:00-10:30", "샘플수업", "A101")
        self.render()

    def render(self):
        # content 영역만 초기화
        for w in self.content.winfo_children():
            w.destroy()

        tt = core.get_timetable()

        frame = ttk.Frame(self.content)
        frame.pack(fill="both", expand=True)

        for day, items in tt.items():
            col = ttk.Frame(frame, relief="groove", borderwidth=1)
            col.pack(side="left", fill="both", expand=True, padx=3)

            ttk.Label(col, text=day.upper()).pack()

            for it in items:
                room = it.get("room", "")
                ttk.Label(col, text=f"{it['time']} {it['name']} ({room})").pack(anchor="w")
