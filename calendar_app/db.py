# calendar_app/db.py
import sqlite3
from typing import List, Dict

from .config import DB_FILE, CATEGORY_DEFS, CATEGORY_PRIORITY


class EventRepository:
    """일정 관련 DB 처리를 전담하는 클래스"""

    def __init__(self, db_path: str = DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    # ---------- 테이블 생성 ----------
    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                start_time TEXT,
                end_time TEXT,
                category TEXT,
                note TEXT
            )
            """
        )
        self.conn.commit()

    # ---------- 기본 CRUD ----------
    def get_events_by_date(self, date_str: str) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id, date, title, start_time, end_time, category, note
            FROM events
            WHERE date = ?
            ORDER BY
                CASE WHEN start_time IS NULL OR start_time = '' THEN 1 ELSE 0 END,
                start_time
            """,
            (date_str,),
        )
        return cur.fetchall()

    def add_event(
        self,
        date_str: str,
        title: str,
        start_time: str,
        end_time: str,
        category: str,
        note: str,
    ) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO events (date, title, start_time, end_time, category, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (date_str, title, start_time, end_time, category, note),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_event(
        self,
        event_id: int,
        title: str,
        start_time: str,
        end_time: str,
        category: str,
        note: str,
    ):
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE events
            SET title = ?, start_time = ?, end_time = ?, category = ?, note = ?
            WHERE id = ?
            """,
            (title, start_time, end_time, category, note, event_id),
        )
        self.conn.commit()

    def delete_event(self, event_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.conn.commit()

    def get_event_note(self, event_id: int) -> str:
        cur = self.conn.cursor()
        cur.execute("SELECT note FROM events WHERE id = ?", (event_id,))
        row = cur.fetchone()
        return row["note"] if row and row["note"] else ""

    # ---------- 캘린더 하이라이트용 ----------
    def get_date_category_map(self) -> Dict[str, str]:
        """
        날짜별로 '가장 강한' 카테고리를 계산해서 dict[date_str, category_key] 로 반환.
        CATEGORY_PRIORITY 순서를 기준으로 우선순위 판단.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT date, category FROM events")
        rows = cur.fetchall()

        date_category: Dict[str, str] = {}
        priority_rank = {key: i for i, key in enumerate(CATEGORY_PRIORITY)}

        for row in rows:
            date_str = row["date"]
            cat = row["category"] or "general"
            if cat not in CATEGORY_DEFS:
                cat = "general"

            if date_str not in date_category:
                date_category[date_str] = cat
            else:
                existing = date_category[date_str]
                # 우선순위 비교 (작을수록 중요)
                if priority_rank.get(cat, 999) < priority_rank.get(existing, 999):
                    date_category[date_str] = cat

        return date_category

    # ---------- 월간 / 검색 ----------
    def get_month_events(self, year: int, month: int) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        month_prefix = f"{year}-{month:02d}"
        cur.execute(
            """
            SELECT date, start_time, end_time, title, category
            FROM events
            WHERE substr(date, 1, 7) = ?
            ORDER BY date, start_time
            """,
            (month_prefix,),
        )
        return cur.fetchall()

    def search_events(
        self,
        keyword: str | None = None,
        category_key: str | None = None,
    ) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        sql = """
            SELECT id, date, start_time, end_time, title, category
            FROM events
        """
        conditions = []
        params: list = []

        if keyword:
            conditions.append("(title LIKE ? OR note LIKE ?)")
            like_kw = f"%{keyword}%"
            params.extend([like_kw, like_kw])

        if category_key:
            conditions.append("category = ?")
            params.append(category_key)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY date, start_time"

        cur.execute(sql, params)
        return cur.fetchall()

    def close(self):
        self.conn.close()
