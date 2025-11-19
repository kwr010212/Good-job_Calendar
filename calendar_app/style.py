# calendar_app/style.py
import tkinter as tk
from tkinter import ttk

from .config import BASE_FONT_FAMILY, BUTTON_BG, BUTTON_BG_ACTIVE, BUTTON_FG


def setup_styles():
    """ttk 기본 스타일(버튼, 트리뷰)을 설정"""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        # 사용 불가한 테마면 무시
        pass

    style.configure(
        "Main.TButton",
        font=(BASE_FONT_FAMILY, 10),
        padding=6,
        background=BUTTON_BG,
        foreground=BUTTON_FG,
        borderwidth=0,
        focusthickness=0,
    )
    style.map(
        "Main.TButton",
        background=[("active", BUTTON_BG_ACTIVE), ("pressed", BUTTON_BG_ACTIVE)],
    )

    style.configure("Treeview", font=(BASE_FONT_FAMILY, 9), rowheight=22)
    style.configure("Treeview.Heading", font=(BASE_FONT_FAMILY, 9, "bold"))

    return style
