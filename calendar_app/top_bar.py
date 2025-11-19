# calendar_app/top_bar.py
import tkinter as tk
from tkinter import ttk

from .config import BASE_FONT_FAMILY


class TopBar(tk.Frame):
    """
    상단 영역: 아이콘 + 제목 + (오늘 / 이번달 목록 / 검색) 버튼들.
    """

    def __init__(self, master, on_today, on_month_list, on_search):
        super().__init__(master, bg="#e0f2fe")

        # 왼쪽: 아이콘 + 앱 이름
        left = tk.Frame(self, bg="#e0f2fe")
        left.pack(side="left", padx=16, pady=8)

        tk.Label(
            left,
            text="📅",
            bg="#e0f2fe",
            fg="#0f172a",
            font=(BASE_FONT_FAMILY, 18),
        ).pack(side="left", padx=(0, 6))

        tk.Label(
            left,
            text="Mint Schedule Calendar",
            bg="#e0f2fe",
            fg="#0f172a",
            font=(BASE_FONT_FAMILY, 14, "bold"),
        ).pack(side="left")

        # 오른쪽: 버튼들
        right = tk.Frame(self, bg="#e0f2fe")
        right.pack(side="right", padx=16, pady=8)

        self.today_btn = ttk.Button(
            right,
            text="오늘",
            command=on_today,
            style="Main.TButton",
            width=8,
        )
        self.today_btn.pack(side="left", padx=4)

        self.month_btn = ttk.Button(
            right,
            text="이번달 목록",
            command=on_month_list,
            style="Main.TButton",
            width=12,
        )
        self.month_btn.pack(side="left", padx=4)

        self.search_btn = ttk.Button(
            right,
            text="검색",
            command=on_search,
            style="Main.TButton",
            width=8,
        )
        self.search_btn.pack(side="left", padx=4)
