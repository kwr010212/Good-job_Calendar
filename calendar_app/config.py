# calendar_app/config.py
# 공통 설정(폰트, 버튼 색, DB 파일, 카테고리 등)

# 전체 앱에서 쓸 기본 폰트
BASE_FONT_FAMILY = "맑은 고딕"  # 여기만 바꾸면 전체 폰트가 바뀜

# 버튼 공통 색상
BUTTON_BG = "#e5e7eb"          # 기본 배경
BUTTON_BG_ACTIVE = "#d4d4d8"   # 눌렀을 때 / 호버 색
BUTTON_FG = "#111827"          # 버튼 글씨 색

# SQLite DB 파일 경로
DB_FILE = "events.db"

# 일정 카테고리 정의
CATEGORY_DEFS = {
    "general":   {"label": "일반",   "color": "#0ea5e9"},
    "school":    {"label": "학교",   "color": "#6366f1"},
    "exam":      {"label": "시험",   "color": "#ef4444"},
    "assignment":{"label": "과제",   "color": "#f97316"},
    "workout":   {"label": "운동",   "color": "#22c55e"},
    "meeting":   {"label": "약속",   "color": "#a855f7"},
    "important": {"label": "중요",   "color": "#db2777"},
}

# 날짜에 색칠할 때 우선순위 (앞에 있는게 더 “센” 카테고리)
CATEGORY_PRIORITY = [
    "important", "exam", "assignment",
    "school", "meeting", "workout", "general"
]
