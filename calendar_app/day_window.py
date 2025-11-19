# calendar_app/day_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt

from .config import BASE_FONT_FAMILY, CATEGORY_DEFS
from .db import EventRepository
from .holidays import get_korean_holidays


class DayWindow(tk.Toplevel):
    """
    특정 날짜의 일정을 추가/수정/삭제하는 창.
    """

    def __init__(
        self,
        master: tk.Tk,
        repo: EventRepository,
        date_obj: dt.date,
        date_str: str,
        on_events_changed,  # 일정 변경 후 호출할 콜백
    ):
        super().__init__(master)
        self.repo = repo
        self.date_obj = date_obj
        self.date_str = date_str
        self.on_events_changed = on_events_changed

        self.title(f"{date_str} 일정")
        self.geometry("500x500")
        self.configure(bg="#f9fafb")
        self.configure(highlightbackground="#cbd5f5", highlightthickness=1)

        # ----- 제목 -----
        weekday_kor = "월화수목금토일"[date_obj.weekday()]

        # 이 날짜가 공휴일이면 이름 가져오기
        year_holidays = get_korean_holidays(date_obj.year)
        holiday_name = year_holidays.get(date_obj, "")

        title_text = f"{date_str} ({weekday_kor})"
        if holiday_name:
            title_text += f" - {holiday_name}"

        # ----- 헤더 -----
        header = tk.Frame(self, bg="#f9fafb")
        header.pack(fill="x", padx=12, pady=(10, 4))

        tk.Label(
            header,
            text=title_text,
            bg="#f9fafb",
            fg="#0f172a",
            font=(BASE_FONT_FAMILY, 12, "bold"),
        ).pack(side="left")

        # ----- 일정 리스트 -----
        list_frame = tk.Frame(self, bg="#f9fafb")
        list_frame.pack(fill="both", expand=False, padx=12, pady=(4, 6))

        columns = ("id", "time", "title", "category")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=7)
        self.tree.heading("id", text="ID")
        self.tree.heading("time", text="시간")
        self.tree.heading("title", text="제목")
        self.tree.heading("category", text="구분")

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("time", width=80, anchor="center")
        self.tree.column("title", width=240, anchor="w")
        self.tree.column("category", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # ----- 입력 폼 -----
        form = tk.Frame(self, bg="#f9fafb")
        form.pack(fill="x", padx=12, pady=(0, 6))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        # 제목
        tk.Label(
            form, text="제목", bg="#f9fafb", fg="#0f172a",
            font=(BASE_FONT_FAMILY, 10)
        ).grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(
            form, textvariable=self.title_var,
            font=(BASE_FONT_FAMILY, 10)
        )
        self.title_entry.grid(row=0, column=1, columnspan=3,
                              sticky="ew", padx=(4, 0), pady=2)

        # 시간 콤보박스
        time_options = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]

        tk.Label(
            form, text="시작", bg="#f9fafb", fg="#0f172a",
            font=(BASE_FONT_FAMILY, 10)
        ).grid(row=1, column=0, sticky="w")
        self.start_var = tk.StringVar(value="09:00")
        start_combo = ttk.Combobox(
            form,
            textvariable=self.start_var,
            values=time_options,
            width=8,
            state="readonly",
        )
        start_combo.grid(row=1, column=1, sticky="w", padx=(4, 10), pady=2)

        tk.Label(
            form, text="끝", bg="#f9fafb", fg="#0f172a",
            font=(BASE_FONT_FAMILY, 10)
        ).grid(row=1, column=2, sticky="w")
        self.end_var = tk.StringVar(value="10:00")
        end_combo = ttk.Combobox(
            form,
            textvariable=self.end_var,
            values=time_options,
            width=8,
            state="readonly",
        )
        end_combo.grid(row=1, column=3, sticky="w", padx=(4, 0), pady=2)

        # 카테고리 + 색
        tk.Label(
            form, text="구분", bg="#f9fafb", fg="#0f172a",
            font=(BASE_FONT_FAMILY, 10)
        ).grid(row=2, column=0, sticky="w")

        self.category_key_var = tk.StringVar(value="general")

        category_labels = [info["label"] for info in CATEGORY_DEFS.values()]
        self.label_to_key = {CATEGORY_DEFS[k]["label"]: k for k in CATEGORY_DEFS}

        self.category_label_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            form,
            textvariable=self.category_label_var,
            values=category_labels,
            state="readonly",
            width=10,
        )
        default_label = CATEGORY_DEFS["general"]["label"]
        self.category_label_var.set(default_label)
        self.category_combo.grid(row=2, column=1, sticky="w",
                                 padx=(4, 10), pady=2)

        self.color_preview = tk.Label(
            form,
            text="●",
            font=(BASE_FONT_FAMILY, 14, "bold"),
            bg="#f9fafb",
            fg=CATEGORY_DEFS["general"]["color"],
        )
        self.color_preview.grid(row=2, column=2, sticky="w", padx=(0, 4))

        self.category_combo.bind("<<ComboboxSelected>>", self._on_category_changed)

        # 메모
        tk.Label(
            form, text="메모", bg="#f9fafb", fg="#0f172a",
            font=(BASE_FONT_FAMILY, 10)
        ).grid(row=3, column=0, sticky="nw")
        self.note_text = tk.Text(
            form, height=3, width=40,
            font=(BASE_FONT_FAMILY, 10),
            bg="#ffffff", fg="#0f172a",
            insertbackground="#0f172a",
        )
        self.note_text.grid(row=3, column=1, columnspan=3,
                            sticky="ew", padx=(4, 0), pady=2)

        # ----- 버튼들 -----
        btn_frame = tk.Frame(self, bg="#f9fafb")
        btn_frame.pack(pady=(4, 10))

        add_btn = ttk.Button(
            btn_frame, text="추가",
            command=self._add_event,
            style="Main.TButton",
        )
        add_btn.grid(row=0, column=0, padx=4)

        update_btn = ttk.Button(
            btn_frame, text="수정",
            command=self._update_event,
            style="Main.TButton",
        )
        update_btn.grid(row=0, column=1, padx=4)

        del_btn = ttk.Button(
            btn_frame, text="삭제",
            command=self._delete_event,
            style="Main.TButton",
        )
        del_btn.grid(row=0, column=2, padx=4)

        clear_btn = ttk.Button(
            btn_frame, text="입력초기화",
            command=self._clear_form,
            style="Main.TButton",
        )
        clear_btn.grid(row=0, column=3, padx=4)

        close_btn = ttk.Button(
            btn_frame, text="닫기",
            command=self.destroy,
            style="Main.TButton",
        )
        close_btn.grid(row=0, column=4, padx=4)

        # 이벤트 바인딩
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        self._refresh_tree()
        self.title_entry.focus_set()

    # ---------- 내부 유틸 ----------
    def _on_category_changed(self, event=None):
        label = self.category_label_var.get()
        key = self.label_to_key.get(label, "general")
        self.category_key_var.set(key)
        self.color_preview.configure(fg=CATEGORY_DEFS[key]["color"])

    def _clear_form(self):
        self.title_var.set("")
        self.start_var.set("09:00")
        self.end_var.set("10:00")
        default_label = CATEGORY_DEFS["general"]["label"]
        self.category_label_var.set(default_label)
        self.category_key_var.set("general")
        self.color_preview.configure(fg=CATEGORY_DEFS["general"]["color"])
        self.note_text.delete("1.0", "end")

    def _refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.repo.get_events_by_date(self.date_str)
        for r in rows:
            event_id = r["id"]
            st = r["start_time"] or ""
            et = r["end_time"] or ""
            if st and et:
                time_disp = f"{st}~{et}"
            elif st:
                time_disp = st
            elif et:
                time_disp = f"~{et}"
            else:
                time_disp = ""

            cat_key = r["category"] or "general"
            cat_label = CATEGORY_DEFS.get(
                cat_key, CATEGORY_DEFS["general"]
            )["label"]

            self.tree.insert(
                "", "end",
                values=(event_id, time_disp, r["title"], cat_label),
            )

    # ---------- CRUD ----------
    def _add_event(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("경고", "제목을 입력하세요.", parent=self)
            return

        start_t = self.start_var.get().strip()
        end_t = self.end_var.get().strip()
        cat_key = self.category_key_var.get() or "general"
        note = self.note_text.get("1.0", "end").strip()

        self.repo.add_event(self.date_str, title, start_t, end_t, cat_key, note)
        self._clear_form()
        self._refresh_tree()
        if self.on_events_changed:
            self.on_events_changed()

    def _delete_event(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("경고", "삭제할 일정을 선택하세요.", parent=self)
            return
        item_id = sel[0]
        vals = self.tree.item(item_id, "values")
        event_id = vals[0]
        if not messagebox.askyesno("삭제 확인", "선택한 일정을 삭제할까요?", parent=self):
            return

        self.repo.delete_event(int(event_id))
        self._refresh_tree()
        if self.on_events_changed:
            self.on_events_changed()

    def _on_tree_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        item_id = sel[0]
        vals = self.tree.item(item_id, "values")
        event_id, time_disp, title, cat_label = vals

        self.title_var.set(title)
        if "~" in time_disp:
            parts = time_disp.split("~")
            self.start_var.set(parts[0])
            self.end_var.set(parts[1])
        else:
            if time_disp:
                self.start_var.set(time_disp)
                self.end_var.set("")
            else:
                self.start_var.set("09:00")
                self.end_var.set("10:00")

        self.category_label_var.set(cat_label)
        key = self.label_to_key.get(cat_label, "general")
        self.category_key_var.set(key)
        self.color_preview.configure(fg=CATEGORY_DEFS[key]["color"])

        note = self.repo.get_event_note(int(event_id))
        self.note_text.delete("1.0", "end")
        if note:
            self.note_text.insert("1.0", note)

    def _update_event(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("경고", "수정할 일정을 선택하세요.", parent=self)
            return
        item_id = sel[0]
        vals = self.tree.item(item_id, "values")
        event_id = vals[0]

        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("경고", "제목을 입력하세요.", parent=self)
            return

        start_t = self.start_var.get().strip()
        end_t = self.end_var.get().strip()
        cat_key = self.category_key_var.get() or "general"
        note = self.note_text.get("1.0", "end").strip()

        self.repo.update_event(int(event_id), title, start_t, end_t, cat_key, note)
        self._refresh_tree()
        if self.on_events_changed:
            self.on_events_changed()
