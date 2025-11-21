import tkinter as tk

# -----------------------------
# 스타일 변수
# -----------------------------
COLOR_BG = "#F7F9FC"
COLOR_NAV = "#3E4A89"
COLOR_BTN = "#5C6BC0"
FONT_MAIN = ("맑은 고딕", 12)

# -----------------------------
# 메인 윈도우 생성
# -----------------------------
root = tk.Tk()
root.title("Campus Timeguard")
root.geometry("1100x700")
root.configure(bg=COLOR_BG)

# -----------------------------
# 네비게이션 바 프레임
# -----------------------------
nav_frame = tk.Frame(root, bg=COLOR_NAV, width=200)
nav_frame.pack(side="left", fill="y")

# -----------------------------
# 메인 화면 프레임
# -----------------------------
main_frame = tk.Frame(root, bg=COLOR_BG)
main_frame.pack(side="right", fill="both", expand=True)

# -----------------------------
# 페이지 전환 함수
# -----------------------------
def clear_main():
    for widget in main_frame.winfo_children():
        widget.destroy()

def show_schedule_page():
    clear_main()
    tk.Label(main_frame, text="일정 페이지(틀)", font=FONT_MAIN).pack(pady=20)

def show_timetable_page():
    clear_main()
    tk.Label(main_frame, text="시간표 페이지(틀)", font=FONT_MAIN).pack(pady=20)

def show_search_page():
    clear_main()
    tk.Label(main_frame, text="검색 페이지(틀)", font=FONT_MAIN).pack(pady=20)

def show_alarm_page():
    clear_main()
    tk.Label(main_frame, text="알림 페이지(틀)", font=FONT_MAIN).pack(pady=20)

# -----------------------------
# 네비게이션 바 버튼
# -----------------------------
tk.Button(nav_frame, text="일정", width=15, bg=COLOR_BTN,
          command=show_schedule_page).pack(pady=10)

tk.Button(nav_frame, text="시간표", width=15, bg=COLOR_BTN,
          command=show_timetable_page).pack(pady=10)

tk.Button(nav_frame, text="검색", width=15, bg=COLOR_BTN,
          command=show_search_page).pack(pady=10)

tk.Button(nav_frame, text="알림", width=15, bg=COLOR_BTN,
          command=show_alarm_page).pack(pady=10)

root.mainloop()
