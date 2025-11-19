# calendar_app/calendar_view.py
import tkinter as tk
from tkcalendar import Calendar
import datetime as dt
import time

from .config import BASE_FONT_FAMILY, CATEGORY_DEFS
from .holidays import get_korean_holidays
from .db import EventRepository


class CalendarView:
    """
    달력(월 뷰)만 담당하는 클래스.
    - 공휴일/일정 하이라이트
    - 월 이동
    - 날짜 더블클릭 콜백
    """

    def __init__(
        self,
        parent: tk.Widget,
        repo: EventRepository,
        on_day_double_click,  # (date_obj, date_str) -> None
    ):
        self.repo = repo
        self.on_day_double_click = on_day_double_click

        self.container = tk.Frame(parent, bg="#f9fafb")

        # 상단(월 표시 + 힌트)
        top_row = tk.Frame(self.container, bg="#f9fafb")
        top_row.pack(fill="x", pady=(6, 0), padx=8)

        self.month_label = tk.Label(
            top_row,
            text="",
            bg="#f9fafb",
            fg="#0f172a",
            font=(BASE_FONT_FAMILY, 12, "bold"),
        )
        self.month_label.pack(side="left")

        

        # 달력 위젯
        cal_frame = tk.Frame(self.container, bg="#f9fafb")
        cal_frame.pack(fill="both", expand=True, padx=8, pady=8)

        today = dt.date.today()
        self.current_year = today.year
        self.holidays = get_korean_holidays(self.current_year)

        self.cal = Calendar(
            cal_frame,
            selectmode="day",
            year=today.year,
            month=today.month,
            day=today.day,
            date_pattern="yyyy-MM-dd",
            background="#ffffff",
            foreground="#111827",
            headersbackground="#0ea5e9",
            headersforeground="white",
            weekendbackground="#f1f5f9",
            weekendforeground="#111827",
            normalbackground="#ffffff",
            disabledforeground="#9ca3af",
            selectbackground="#0ea5e9",
            selectforeground="white",
            bordercolor="#e5e7eb",
            showweeknumbers=False,
            firstweekday="sunday",
            font=(BASE_FONT_FAMILY, 10),
        )
        self.cal.pack(fill="both", expand=True)

        # 더블클릭 판정용
        self.last_click_date = None
        self.last_click_time = 0.0

        # 태그 설정 & 초기 하이라이트
        self._setup_calendar_tags()
        self.refresh_event_highlight()
        self.refresh_holiday_highlight()
        self.update_month_label()

        # 바인딩
        self.cal.bind("<<CalendarSelected>>", self._on_day_click)
        self.cal.bind("<<CalendarMonthChanged>>", self._on_month_changed)

    # ---------- 태그 / 색 ----------
    def _setup_calendar_tags(self):
        self.cal.tag_config("holiday", background="#fee2e2", foreground="#b91c1c")
        for key, info in CATEGORY_DEFS.items():
            self.cal.tag_config(
                f"cat_{key}", background=info["color"], foreground="white"
            )
        self.cal.tag_config("event_generic", background="#dbeafe", foreground="#111827")

    def refresh_holiday_highlight(self):
        self.cal.calevent_remove(tag="holiday")
        for date_obj, name in self.holidays.items():
            self.cal.calevent_create(date_obj, name, "holiday")

    def refresh_event_highlight(self):
        # 기존 일정 태그 제거
        for key in CATEGORY_DEFS.keys():
            self.cal.calevent_remove(tag=f"cat_{key}")
        self.cal.calevent_remove(tag="event_generic")

        date_category = self.repo.get_date_category_map()
        for date_str, cat in date_category.items():
            try:
                y, m, d = map(int, date_str.split("-"))
                date_obj = dt.date(y, m, d)
            except ValueError:
                continue

            tag_name = f"cat_{cat}" if cat in CATEGORY_DEFS else "event_generic"
            self.cal.calevent_create(date_obj, "", tag_name)

    def update_month_label(self):
        m, y = self.cal.get_displayed_month()
        self.month_label.config(text=f"{y}년 {m}월")

    # ---------- 월 이동 / 오늘 ----------
    def _on_month_changed(self, event=None):
        month, year = self.cal.get_displayed_month()
        if year != self.current_year:
            self.current_year = year
            self.holidays = get_korean_holidays(self.current_year)
        self.refresh_event_highlight()
        self.refresh_holiday_highlight()
        self.update_month_label()

    def go_today(self):
        today = dt.date.today()
        self.cal.selection_set(today)
        self.cal.see(today)
        self.update_month_label()

    def get_displayed_month(self):
        return self.cal.get_displayed_month()

    def see_date(self, date_obj: dt.date):
        self.cal.selection_set(date_obj)
        self.cal.see(date_obj)
        self.update_month_label()

    # ---------- 날짜 더블클릭 ----------
    def _on_day_click(self, event=None):
        date_obj = self.cal.selection_get()
        if not isinstance(date_obj, dt.date):
            return

        now = time.time()
        if self.last_click_date == date_obj and (now - self.last_click_time) < 0.5:
            # 더블클릭 판정
            date_str = date_obj.strftime("%Y-%m-%d")
            if self.on_day_double_click:
                self.on_day_double_click(date_obj, date_str)

        self.last_click_date = date_obj
        self.last_click_time = now
