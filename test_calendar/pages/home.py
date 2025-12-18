# pages/home.py
import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        ttk.Label(self, text="간단 일정관리 - 홈", font=("Arial", 18)).pack(pady=12)

        buttons = [
            ("달력", "Calendar"),
            ("일정 등록/수정", "Register"),
            ("시간표", "Timetable"),
            ("검색/필터", "Search"),
            ("알림", "Notify")
        ]
        for txt, name in buttons:
            b = ttk.Button(self, text=txt, command=lambda n=name: controller.show(n))
            b.pack(fill="x", padx=120, pady=6)
