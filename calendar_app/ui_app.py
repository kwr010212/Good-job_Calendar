# calendar_app/ui_app.py
import tkinter as tk
from tkinter import ttk

from .config import BASE_FONT_FAMILY
from .style import setup_styles
from .db import EventRepository
from .calendar_view import CalendarView
from .day_window import DayWindow
from .month_list import MonthListWindow
from .search_window import SearchWindow
from .top_bar import TopBar
from .status_bar import StatusBar


class MintCalendarApp:
    """
    전체 앱을 조립하는 메인 클래스.

    책임:
    - Tk 루트(window) 기본 설정
    - 공통 스타일 세팅
    - 상단 TopBar / 중앙 CalendarView / 하단 StatusBar 배치
    - 버튼과 서브 윈도우(DayWindow, MonthListWindow, SearchWindow) 연결
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mint Schedule Calendar")
        self.root.geometry("620x720")
        self.root.configure(bg="#e0f2fe")  # 밝은 하늘색 배경

        # ttk 스타일 설정
        setup_styles()

        # DB 리포지토리
        self.repo = EventRepository()

        # ----- 상단 TopBar (아이콘 + 제목 + 버튼들) -----
        self.top_bar = TopBar(
            self.root,
            on_today=self.go_today,
            on_month_list=self.open_month_list_window,
            on_search=self.open_search_window,
        )
        self.top_bar.pack(fill="x", pady=(6, 0))

        # ----- 힌트 라벨 -----
        hint_frame = tk.Frame(self.root, bg="#e0f2fe")
        hint_frame.pack(fill="x", pady=(4, 0), padx=12)

        tk.Label(
            hint_frame,
            text="날짜를 빠르게 두 번 클릭하면 일정 창이 열립니다.",
            bg="#e0f2fe",
            fg="#334155",
            font=(BASE_FONT_FAMILY, 9),
        ).pack(anchor="e")

        # ----- 중앙 달력 뷰 -----
        self.calendar_view = CalendarView(
            self.root,
            repo=self.repo,
            on_day_double_click=self.open_day_window,
        )
        self.calendar_view.container.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(4, 8),
        )

        # ----- 하단 상태바 -----
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(fill="x", padx=0, pady=(0, 0))

        # 초기 상태 메시지
        self.status_bar.set_message(
            "Tip: 날짜 더블클릭으로 일정창 열기 / '오늘' 버튼으로 오늘로 이동"
        )

    # ------------------------------------------------------------------
    # 달력 색칠 업데이트 (일정 변경 시 DayWindow에서 콜백)
    # ------------------------------------------------------------------
    def refresh_event_highlight(self):
        """일정이 변경되었을 때 달력 색칠만 새로고침"""
        self.calendar_view.refresh_event_highlight()

    # ------------------------------------------------------------------
    # TopBar 버튼에서 호출되는 메서드
    # ------------------------------------------------------------------
    def go_today(self):
        """오늘 날짜로 캘린더 이동"""
        self.calendar_view.go_today()

    def open_day_window(self, date_obj, date_str: str):
        """특정 날짜의 일정 창 열기 (달력 더블클릭에서 호출)"""
        DayWindow(
            self.root,
            repo=self.repo,
            date_obj=date_obj,
            date_str=date_str,
            on_events_changed=self.refresh_event_highlight,
        )

    def open_month_list_window(self):
        """현재 표시중인 달의 일정 목록 창"""
        month, year = self.calendar_view.get_displayed_month()
        MonthListWindow(
            self.root,
            repo=self.repo,
            year=year,
            month=month,
            open_day_window=self._open_day_window_and_focus,
        )

    def open_search_window(self):
        """검색 창 열기"""
        SearchWindow(
            self.root,
            repo=self.repo,
            open_day_window=self._open_day_window_and_focus,
        )

    # ------------------------------------------------------------------
    # 검색/월 목록에서 날짜 더블클릭 시 호출되는 헬퍼
    # ------------------------------------------------------------------
    def _open_day_window_and_focus(self, date_obj, date_str: str):
        """
        검색창/월목록에서 더블클릭했을 때 호출.
        - 메인 달력에서 해당 날짜가 보이도록 스크롤 후
        - DayWindow를 띄운다.
        """
        self.calendar_view.see_date(date_obj)
        self.open_day_window(date_obj, date_str)
