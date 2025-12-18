# core.py
"""
통합 핵심 모듈 (저장, 일정 CRUD, 검색, 달력 계산, 시간표, 알림)
저장 포맷: data.json (리스트 형태의 dict 들)
각 일정은 딕셔너리로 저장되며, id가 부여됩니다.
필수 필드: id, title, date (YYYY-MM-DD)
옵션: time (HH:MM), category, memo, alarm (bool)
"""

import json
import os
from datetime import datetime, date, timedelta
import calendar
from typing import List, Dict, Any

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# 내부 메모리 구조: id -> item(dict)
_store: Dict[int, Dict[str, Any]] = {}
_next_id = 1

# ----------------- 파일 입출력 -----------------
def _load_file():
    global _store, _next_id
    if not os.path.exists(DATA_FILE):
        _store = {}
        _next_id = 1
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    _store = {int(item["id"]): item for item in data if "id" in item}
    _next_id = max(_store.keys()) + 1 if _store else 1

def _save_file():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(list(_store.values()), f, ensure_ascii=False, indent=2)

# ----------------- 저장/CRUD -----------------
def load_all() -> List[Dict[str, Any]]:
    """파일에서 읽어 메모리 동기화 후 리스트 반환"""
    _load_file()
    return list(_store.values())

def get_all() -> List[Dict[str, Any]]:
    """메모리상의 전체 일정 반환(간단 조회)"""
    return list(_store.values())

def add(item: Dict[str, Any]) -> Dict[str, Any]:
    """새 항목 추가, id 자동 부여"""
    global _next_id
    _load_file()  # ensure synced
    item = dict(item)
    item_id = _next_id
    item["id"] = item_id
    _store[item_id] = item
    _next_id += 1
    _save_file()
    return item

def update(item_id: int, new_item: Dict[str, Any]) -> bool:
    _load_file()
    if item_id not in _store:
        return False
    new_item = dict(new_item)
    new_item["id"] = item_id
    _store[item_id] = new_item
    _save_file()
    return True

def delete(item_id: int) -> bool:
    _load_file()
    if item_id in _store:
        del _store[item_id]
        _save_file()
        return True
    return False

def find_by_id(item_id: int):
    _load_file()
    return _store.get(item_id)

# ----------------- schedule 래퍼 -----------------
def add_schedule(title: str, date_str: str, time_str: str = "", category: str = "", memo: str = "", alarm: bool = False) -> Dict[str, Any]:
    item = {
        "title": title,
        "date": date_str,
        "time": time_str,
        "category": category,
        "memo": memo,
        "alarm": bool(alarm)
    }
    return add(item)

def update_schedule(item_id: int, **fields) -> bool:
    old = find_by_id(item_id)
    if not old:
        return False
    new = dict(old)
    new.update(fields)
    return update(item_id, new)

def delete_schedule(item_id: int) -> bool:
    return delete(item_id)

def get_all_schedules() -> List[Dict[str, Any]]:
    return load_all()

# ----------------- 검색/필터 -----------------
def search_keyword(keyword: str) -> List[Dict[str, Any]]:
    items = get_all()
    kw = keyword.lower()
    return [it for it in items if kw in it.get("title","").lower() or kw in it.get("memo","").lower()]

def filter_by_date(start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    items = get_all()
    if not start_date and not end_date:
        return items
    res = []
    for it in items:
        d = it.get("date")
        if not d:
            continue
        if start_date and d < start_date:
            continue
        if end_date and d > end_date:
            continue
        res.append(it)
    return res

def filter_by_category(category: str) -> List[Dict[str, Any]]:
    items = get_all()
    return [it for it in items if it.get("category","") == category]

# ----------------- 달력 계산 -----------------
def get_month_matrix(year: int, month: int) -> List[List[Dict[str, str]]]:
    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    weeks = []
    for week in cal.monthdatescalendar(year, month):
        week_row = []
        for d in week:
            if d.month != month:
                week_row.append({'day': 0, 'date_str': ''})
            else:
                week_row.append({'day': d.day, 'date_str': d.isoformat()})
        weeks.append(week_row)
    return weeks

def today_str() -> str:
    return date.today().isoformat()

# ----------------- 시간표 (간단) -----------------
_timetable = {
    'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': [], 'sat': [], 'sun': []
}

def add_class(day: str, time_range: str, name: str, room: str = ""):
    key = day.lower()[:3]
    if key not in _timetable:
        raise ValueError("Invalid day")
    _timetable[key].append({'time': time_range, 'name': name, 'room': room})
    return True

def remove_class(day: str, index: int):
    key = day.lower()[:3]
    if key not in _timetable or index >= len(_timetable[key]):
        return False
    _timetable[key].pop(index)
    return True

def get_timetable():
    return _timetable

# ----------------- 알림 -----------------
def upcoming_alerts(within_minutes: int = 60) -> List[Dict[str, Any]]:
    now = datetime.now()
    limit = now + timedelta(minutes=within_minutes)
    result = []
    for it in get_all():
        if not it.get("alarm"):
            continue
        d = it.get("date")
        t = it.get("time", "")
        if not d or not t:
            continue
        try:
            dt = datetime.fromisoformat(f"{d}T{t}")
        except Exception:
            # 허용되지 않는 형식이면 skip
            continue
        if now <= dt <= limit:
            result.append(it)
    return result

# ----------------- 간단한 유효성(도움) -----------------
def is_valid_date(s: str) -> bool:
    try:
        datetime.fromisoformat(s)
        return True
    except Exception:
        return False
