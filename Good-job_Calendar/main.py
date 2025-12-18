import tkinter as tk
from tkinter import ttk

from pages.home import HomePage
from pages.register import RegisterPage
from pages.calendar import CalendarPage
from pages.search import SearchPage
from pages.timetable import TimetablePage
from pages.notify import NotifyPage


NAVY = "#0A1F44"
WHITE = "#FFFFFF"


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ===== 기본 창 설정 =====
        self.title("Campus Calendar")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(background=NAVY)

        # ===== 스타일 설정 =====
        self._set_style()

        # ===== 메인 컨테이너 =====
        self.container = ttk.Frame(self, style="Main.TFrame")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # ===== 페이지(Frame) 관리 =====
        self.frames = {}
        self._register_pages()

        # 첫 화면
        self.show("Home")

    def _set_style(self):
        style = ttk.Style()
        style.theme_use("default")

        # 전체 앱 배경
        style.configure(
            "Main.TFrame",
            background=NAVY
        )

        # 페이지 카드 (화이트)
        style.configure(
            "TFrame",
            background=WHITE,
            relief="flat"
        )

        # 기본 텍스트
        style.configure(
            "TLabel",
            background=WHITE,
            foreground=NAVY,
            font=("맑은 고딕", 11)
        )

        # 제목 텍스트 (앱 타이틀 느낌)
        style.configure(
            "Title.TLabel",
            background=WHITE,
            foreground=NAVY,
            font=("맑은 고딕", 20, "bold")
        )

        # 버튼 (심플한 네이비 텍스트)
        style.configure(
            "TButton",
            background=WHITE,
            foreground=NAVY,
            font=("맑은 고딕", 10, "bold"),
            padding=(14, 8),
            relief="flat"
        )

        style.map(
            "TButton",
            background=[
                ("active", WHITE),
                ("pressed", WHITE)
            ],
            foreground=[
                ("active", NAVY),
                ("pressed", NAVY)
            ]
        )

    def _register_pages(self):
        pages = {
            "Home": HomePage,
            "Register": RegisterPage,
            "Calendar": CalendarPage,
            "Search": SearchPage,
            "Timetable": TimetablePage,
            "Notify": NotifyPage
        }

        for name, PageClass in pages.items():
            frame = PageClass(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.frames[name] = frame

    def show(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
