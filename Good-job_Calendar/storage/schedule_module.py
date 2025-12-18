# pages/register.py
import tkinter as tk
from tkinter import ttk, messagebox
import core

class RegisterPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        ttk.Label(self, text="일정 등록 / 수정", font=("Arial", 16)).pack(pady=8)

        frm = ttk.Frame(self)
        frm.pack(padx=12, pady=6, fill="x")

        self.id_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.cat_var = tk.StringVar()
        self.memo_var = tk.StringVar()
        self.alarm_var = tk.BooleanVar()

        rows = [
            ("ID(수정용)", self.id_var),
            ("제목", self.title_var),
            ("날짜 (YYYY-MM-DD)", self.date_var),
            ("시간 (HH:MM)", self.time_var),
            ("카테고리", self.cat_var),
            ("메모", self.memo_var)
        ]
        for label, var in rows:
            r = ttk.Frame(frm); r.pack(fill="x", pady=3)
            ttk.Label(r, text=label, width=16).pack(side="left")
            ttk.Entry(r, textvariable=var).pack(side="left", fill="x", expand=True)

        ttk.Checkbutton(frm, text="알림", variable=self.alarm_var).pack(pady=6)

        btns = ttk.Frame(self); btns.pack(pady=8)
        ttk.Button(btns, text="저장", command=self.save).pack(side="left", padx=6)
        ttk.Button(btns, text="삭제(ID로)", command=self.delete_by_id).pack(side="left", padx=6)
        ttk.Button(btns, text="홈", command=lambda: controller.show("Home")).pack(side="left", padx=6)
        ttk.Button(btns, text="새로고침(목록)", command=self.load_all).pack(side="left", padx=6)

        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=6)
        self.load_all()

    def save(self):
        id_text = self.id_var.get().strip()
        title = self.title_var.get().strip()
        date_s = self.date_var.get().strip()
        time_s = self.time_var.get().strip()
        cat = self.cat_var.get().strip()
        memo = self.memo_var.get().strip()
        alarm = self.alarm_var.get()

        if not title or not date_s:
            messagebox.showwarning("입력 오류", "제목과 날짜는 필수입니다.")
            return

        try:
           
            datetime_obj = core.datetime.fromisoformat(date_s)
            
        except Exception:
          
            try:
                core.date.fromisoformat(date_s)
            except Exception:
                messagebox.showerror("오류", "날짜 형식은 YYYY-MM-DD 이어야 합니다.")
                return

        if id_text:
            try:
                item_id = int(id_text)
            except ValueError:
                messagebox.showerror("오류", "ID는 숫자여야 합니다.")
                return
            ok = core.update_schedule(item_id, title=title, date=date_s, time=time_s, category=cat, memo=memo, alarm=alarm)
            if ok:
                messagebox.showinfo("수정", "일정이 수정되었습니다.")
            else:
                messagebox.showerror("오류", "해당 ID가 없습니다.")
        else:
            core.add_schedule(title=title, date_str=date_s, time_str=time_s, category=cat, memo=memo, alarm=alarm)
            messagebox.showinfo("저장", "일정이 추가되었습니다.")
        self.load_all()

    def delete_by_id(self):
        id_text = self.id_var.get().strip()
        if not id_text:
            messagebox.showwarning("입력 오류", "삭제하려면 ID를 입력하세요.")
            return
        try:
            item_id = int(id_text)
        except ValueError:
            messagebox.showerror("오류", "ID는 숫자여야 합니다.")
            return
        ok = core.delete_schedule(item_id)
        if ok:
            messagebox.showinfo("삭제", "일정이 삭제되었습니다.")
            self.load_all()
        else:
            messagebox.showerror("오류", "해당 ID가 없습니다.")

    def load_all(self):
        items = core.get_all_schedules()
        self.listbox.delete(0, "end")
        for it in items:
            txt = f"{it['id']}: {it['date']} {it.get('time','')} - {it.get('title','')} [{it.get('category','')}]"
            self.listbox.insert("end", txt)