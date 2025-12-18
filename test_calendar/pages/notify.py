# pages/notify.py
import tkinter as tk
from tkinter import ttk, messagebox
import core

class NotifyPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        ttk.Label(self, text="알림", font=("Arial", 16)).pack(pady=8)
        ttk.Button(self, text="홈", command=lambda: controller.show("Home")).pack(pady=4)
        ttk.Button(self, text="향후 60분 알림 확인", command=self.check_now).pack(pady=4)

        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(fill="both", expand=True, padx=8, pady=6)

    def check_now(self):
        items = core.upcoming_alerts(60)
        self.listbox.delete(0, "end")
        if not items:
            messagebox.showinfo("알림", "향후 60분 내 알람 일정이 없습니다.")
            return
        for it in items:
            self.listbox.insert("end", f"{it['date']} {it.get('time','')} - {it['title']}")
