# calendar_app/status_bar.py
import tkinter as tk

from .config import BASE_FONT_FAMILY


class StatusBar(tk.Frame):
    """
    하단 상태 표시줄.
    - 간단한 도움말/상태 텍스트를 보여준다.
    """

    def __init__(self, master):
        super().__init__(master, bg="#e0f2fe")
        self.label = tk.Label(
            self,
            text="",
            anchor="w",
            bg="#e0f2fe",
            fg="#64748b",
            font=(BASE_FONT_FAMILY, 9),
        )
        self.label.pack(fill="x", padx=12, pady=4)

    def set_message(self, text: str):
        self.label.config(text=text)
