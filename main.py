# 임시 main.py
import tkinter as tk
from tkinter import messagebox
import woorim as sm

# 테스트 data[딕셔너리 사용]
schedule_list = [
    {"id": 1, "title": "프로젝트 발표", "date": "2025-11-21", "tag": "발표"},
    {"id": 2, "title": "기말고사", "date": "2025-12-16", "tag": "시험"},
]

# 검색 처리 함수
def perform_search():
    date = entry_date.get()
    keyword = entry_keyword.get()
    tag = entry_tag.get()

    result = sm.search(
        schedule_list,
        date=date if date else None,
        keyword=keyword if keyword else None,
        tag=tag if tag else None
    )

    listbox_result.delete(0, tk.END)

    if not result:
        listbox_result.insert(tk.END, "검색 결과가 없습니다.")
    else:
        for item in result:
            text = f"[{item['id']}] {item['date']} | {item['title']} | {item['student']} | {item['tag']}"
            listbox_result.insert(tk.END, text)



# 임시 ui
window = tk.Tk()
window.title("학생 일정 검색")
window.geometry("500x450")

# 날짜 입력
tk.Label(window, text="날짜 (YYYY-MM-DD)").pack()
entry_date = tk.Entry(window)
entry_date.pack()

# 제목 키워드
tk.Label(window, text="제목 키워드").pack()
entry_keyword = tk.Entry(window)
entry_keyword.pack()

# 태그
tk.Label(window, text="태그").pack()
entry_tag = tk.Entry(window)
entry_tag.pack()

# 검색 버튼
tk.Button(window, text="검색", command=perform_search).pack(pady=10)

# 검색 결과
listbox_result = tk.Listbox(window, width=30)
listbox_result.pack(pady=10)

window.mainloop()