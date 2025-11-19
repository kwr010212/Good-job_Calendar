# mid_gui.py  - 중간 발표용 GUI

import tkinter as tk

# -----------------------------
# 스타일 색상
# -----------------------------
COLOR_BG = "#EEF2F7"            
COLOR_NAV = "#283593"          
COLOR_NAV_HOVER = "#3949AB"
COLOR_CARD = "#FFFFFF"          
COLOR_BTN = "#5667FF"
COLOR_BTN_HOVER = "#6F7BFF"


class CampusTimeguardMidGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Campus Timeguard - Mid")
        self.root.geometry("1300x800")
        self.root.configure(bg=COLOR_BG)

        self.root.option_add("*Font", ("맑은고딕", 10))

        self.create_navbar()

        self.main_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.main_frame.pack(fill="both", expand=True)

        self.show_home()

        self.root.mainloop()

    # -----------------------------
    # NAVIGATION (심플 버전)
    # -----------------------------
    def create_navbar(self):
        nav = tk.Frame(self.root, bg=COLOR_NAV, height=60)
        nav.pack(fill="x")

        menus = {
            "홈": self.show_home,
            "일정 관리": self.show_schedule_page,
            "시간표": self.show_timetable_page,
            "달력": self.show_calendar_page,
            "데이터": self.show_data_page,
            "알림": self.show_alarm_page,
            "검색": self.show_search_page
        }

        for name, func in menus.items():
            btn = tk.Label(nav, text=name, padx=20, pady=17,
                           bg=COLOR_NAV, fg="white", cursor="hand2",
                           font=("맑은고딕", 11, "bold"))
            btn.pack(side="left")

            btn.bind("<Button-1>", lambda e, f=func: f())
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_NAV_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_NAV))

    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    # -----------------------------
    # HOME
    # -----------------------------
    def show_home(self):
        self.clear_main()

        tk.Label(
            self.main_frame,
            text="Campus Timeguard",
            font=("맑은고딕", 32, "bold"),
            bg=COLOR_BG,
            fg="#1E2A5A"
        ).pack(pady=60)

        card = tk.Frame(
            self.main_frame,
            bg=COLOR_CARD,
            bd=2,
            relief="solid",
            padx=40,
            pady=30
        )
        card.pack(ipadx=60, ipady=25)

        tk.Label(
            card,
            text="대학생을 위한 일정 · 시간표 · 알림 통합 관리 프로그램",
            font=("맑은고딕", 15, "bold"),
            bg=COLOR_CARD
        ).pack(pady=(0, 12))

        tk.Label(
            card,
            text="캠퍼스 라이프를 더 편하게, 더 스마트하게.",
            font=("맑은고딕", 12),
            fg="#555",
            bg=COLOR_CARD
        ).pack()

    # -----------------------------
    # 일정 관리 (틀만)
    # -----------------------------
    def show_schedule_page(self):
        self.clear_main()

        tk.Label(self.main_frame, text=" 일정 관리",
                 font=("맑은고딕", 20, "bold"),
                 bg=COLOR_BG).pack(pady=10)

        tk.Label(self.main_frame,
                 text="개인 일정을 등록 / 수정 / 삭제할 수 있는 화면입니다.",
                 bg=COLOR_BG, fg="#555").pack()

        container = tk.Frame(self.main_frame, bg=COLOR_BG)
        container.pack(fill="both", expand=True)

        # 좌측 입력 폼
        left = tk.Frame(container, bg=COLOR_CARD, bd=1, relief="solid")
        left.pack(side="left", fill="y", padx=40, pady=25, ipadx=10, ipady=10)

        tk.Label(left, text="일정 등록", font=("맑은고딕", 13, "bold"),
                 bg=COLOR_CARD).pack(pady=10)

        self.create_form(left, "제목")
        self.create_form(left, "날짜")
        self.create_form(left, "내용")

        self.create_button(left, "등록")
        self.create_button(left, "수정")
        self.create_button(left, "삭제")

        # 우측 목록
        right = tk.Frame(container, bg=COLOR_CARD, bd=1, relief="solid")
        right.pack(side="left", fill="both", expand=True,
                   padx=20, pady=25)

        tk.Label(right, text="일정 목록",
                 font=("맑은고딕", 13, "bold"),
                 bg=COLOR_CARD).pack(pady=10)

        scrollbar = tk.Scrollbar(right)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(right, yscrollcommand=scrollbar.set,
                             bg=COLOR_CARD, font=("맑은고딕", 11))
        listbox.pack(fill="both", expand=True, padx=15, pady=15)
        scrollbar.config(command=listbox.yview)

    # -----------------------------
    # 시간표 (PPT 스타일, 편집 기능 X)
    # -----------------------------
    def show_timetable_page(self):
        self.clear_main()

        tk.Label(self.main_frame, text="Class Time Table",
                 font=("맑은고딕", 24, "bold"),
                 bg=COLOR_BG).pack(pady=20)

        tk.Label(self.main_frame,
                 text="주간 시간표를 확인하기 위한 화면입니다.",
                 bg=COLOR_BG, fg="#555").pack()

        card = tk.Frame(self.main_frame, bg=COLOR_CARD, bd=1, relief="solid")
        card.pack(pady=15, padx=30, ipadx=10, ipady=10)

        table = tk.Frame(card, bg=COLOR_CARD)
        table.pack()

        days = ["교시", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        hours = ["1교시", "2교시", "3교시", "4교시",
                 "점심시간",
                 "5교시", "6교시", "7교시", "8교시"]

        # 헤더
        for col, day in enumerate(days):
            tk.Label(table, text=day,
                     width=14, height=2,
                     bg="#3B5998", fg="white",
                     font=("맑은고딕", 12, "bold"),
                     relief="solid").grid(row=0, column=col, padx=1, pady=1)

        row_index = 1
        for h in hours:
            if h == "점심시간":
                tk.Label(table, text=h,
                         width=100, height=2,
                         bg=COLOR_CARD, fg="#555",
                         font=("맑은고딕", 12, "bold"),
                         relief="solid").grid(row=row_index, column=0,
                                              columnspan=len(days),
                                              padx=1, pady=8)
                row_index += 1
                continue

            tk.Label(table, text=h,
                     width=14, height=2,
                     bg=COLOR_CARD,
                     font=("맑은고딕", 11, "bold"),
                     relief="solid").grid(row=row_index, column=0,
                                          padx=1, pady=1)

            for col in range(1, len(days)):
                tk.Label(table, text="",
                         width=14, height=3,
                         bg="white",
                         relief="solid",
                         font=("맑은고딕", 10)).grid(row=row_index, column=col,
                                                     padx=1, pady=1)
            row_index += 1

    # -----------------------------
    # 달력 / 데이터 / 알림 / 검색 (틀만)
    # -----------------------------
    def show_calendar_page(self):
        self.clear_main()
        tk.Label(self.main_frame, text="달력",
                 font=("맑은고딕", 20, "bold"),
                 bg=COLOR_BG).pack(pady=20)
        tk.Label(self.main_frame,
                 text="팀원이 구현한 달력 기능이 연결될 예정입니다.",
                 bg=COLOR_BG, fg="#555").pack()

    def show_data_page(self):
        self.clear_main()
        tk.Label(self.main_frame, text="데이터 저장 / 불러오기",
                 font=("맑은고딕", 20, "bold"),
                 bg=COLOR_BG).pack(pady=20)
        self.create_button(self.main_frame, "데이터 저장")
        self.create_button(self.main_frame, "데이터 불러오기")

    def show_alarm_page(self):
        self.clear_main()
        tk.Label(self.main_frame, text="알림 기능",
                 font=("맑은고딕", 20, "bold"),
                 bg=COLOR_BG).pack(pady=20)
        tk.Label(self.main_frame,
                 text="알림 시간 설정 및 알림 목록이 표시될 예정입니다.",
                 bg=COLOR_BG, fg="#555").pack()

    def show_search_page(self):
        self.clear_main()
        tk.Label(self.main_frame, text="일정 검색",
                 font=("맑은고딕", 20, "bold"),
                 bg=COLOR_BG).pack(pady=20)
        entry = tk.Entry(self.main_frame, width=40)
        entry.pack(pady=5)
        self.create_button(self.main_frame, "검색")

    # -----------------------------
    # 재사용 컴포넌트
    # -----------------------------
    def create_form(self, parent, text):
        tk.Label(parent, text=text, bg=COLOR_CARD).pack(anchor="w")
        entry = tk.Entry(parent, width=30)
        entry.pack(pady=5)

    def create_button(self, parent, text):
        btn = tk.Button(parent, text=text, bg=COLOR_BTN, fg="white",
                        activebackground=COLOR_BTN_HOVER, width=20)
        btn.pack(pady=6)
        return btn


if __name__ == "__main__":
    CampusTimeguardMidGUI()
