# pages/search.py
import tkinter as tk
from tkinter import ttk
import core

class SearchPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        ttk.Label(self, text="검색 / 필터", font=("Arial", 16)).pack(pady=8)
        top = ttk.Frame(self); top.pack(fill="x", padx=8)
        self.q = tk.StringVar()
        ttk.Entry(top, textvariable=self.q).pack(side="left", fill="x", expand=True)
        ttk.Button(top, text="검색", command=self.do_search).pack(side="left", padx=4)
        ttk.Button(top, text="전체 보기", command=self.load_all).pack(side="left", padx=4)
        ttk.Button(top, text="홈", command=lambda: controller.show("Home")).pack(side="left", padx=4)

        self.listbox = tk.Listbox(self, height=14)
        self.listbox.pack(fill="both", expand=True, padx=8, pady=6)
        self.load_all()

    def do_search(self):
        q = self.q.get().strip()
        if not q:
            self.load_all(); return
        items = core.search_keyword(q)
        self.listbox.delete(0, "end")
        for it in items:
            self.listbox.insert("end", f"{it['id']}: {it['date']} {it.get('time','')} - {it['title']}")

    def load_all(self):
        items = core.get_all_schedules()
        self.listbox.delete(0, "end")
        for it in items:
            self.listbox.insert("end", f"{it['id']}: {it['date']} {it.get('time','')} - {it['title']}")
