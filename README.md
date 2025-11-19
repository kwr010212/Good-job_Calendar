
🗂️ 프로젝트 구조
calendar_app/
│
├─ ui_app.py
├─ calendar_view.py
├─ day_window.py
├─ month_list.py
├─ search_window.py
│
├─ top_bar.py
├─ status_bar.py
│
├─ holidays.py
├─ db.py
├─ config.py
├─ style.py
│
├─ __init__.py
└─ events.db (자동 생성)
│
run_calendar.py
README.md




---

# 📦 Module Structure (모듈 구조 설명)

아래는 `calendar_app` 패키지 내부 모듈들의 역할을 한눈에 이해할 수 있도록 정리한 구조 설명입니다.

---

## 🧩 1. ui_app.py — **전체 앱 조립(메인 컨트롤러)**

* 앱 전체 UI를 배치하고 조립하는 메인 컨트롤러
* TopBar / CalendarView / StatusBar 연결
* 오늘 버튼, 검색, 이번달 리스트 등 주요 기능 제어
* 일정 창(DayWindow), 검색창(SearchWindow), 월 리스트(MonthList) 호출 담당

> 전체 앱의 “두뇌” 역할

---

## 📅 2. calendar_view.py — **달력 화면 렌더링**

* 월별 달력 그리기
* 이전/다음달 이동 기능
* 공휴일 표시
* 일정이 있는 날짜 하이라이트
* 날짜 더블클릭 → DayWindow 열기

> 실제 달력 UI를 담당하는 핵심 화면

---

## 🗓️ 3. day_window.py — **날짜별 일정 CRUD 창**

* 특정 날짜의 일정 추가/수정/삭제
* 시간 선택, 카테고리, 메모 입력
* 일정 변경 시 달력 이벤트 하이라이트 업데이트

> 하루 일정 관리 기능 담당

---

## 📋 4. month_list.py — **이번달 전체 일정 목록 보기**

* 이번 달 전체 일정을 테이블 형태로 출력
* 일정 더블클릭 → 해당 날짜 DayWindow로 이동

> 달 전체 일정 관리를 위한 리스트 화면

---

## 🔍 5. search_window.py — **일정 검색창**

* 일정 제목/내용 검색 기능
* 검색 결과 목록화
* 결과 더블클릭 → 해당 날짜 일정 관리창 이동

> 프로젝트의 검색 엔진 역할

---

## 🎚️ 6. top_bar.py — **상단 메뉴 UI**

* 앱 제목, 오늘 버튼, 검색창 열기, 이번달 목록 버튼 등 관리
* 단순하고 깔끔한 상단 네비게이션

> 화면 최상단의 메뉴 구성 담당

---

## 📢 7. status_bar.py — **하단 상태 표시줄**

* 사용자에게 도움말/상태 메시지를 표시
* 예) "Tip: 날짜 더블클릭 시 일정창 열림"

> 작은 설명과 상태 안내

---

## 🎌 8. holidays.py — **한국 공휴일 계산 모듈**

* 특정 연도의 공휴일 자동 계산
* calendar_view에서 불러와 달력에 표시됨

> 공휴일 설정/관리 기능

---

## 🗃️ 9. db.py — **SQLite 일정 데이터 저장소**

* SQLite를 이용한 일정 CRUD 저장
* events.db 파일 생성/관리
* 검색창/달력/날짜창 등 모든 모듈이 사용하는 중심 DB

> 전체 일정의 데이터베이스 관리자

---

## ⚙️ 10. config.py — **앱 공용 설정파일**

* 기본 폰트, 테마 색상, 앱 스타일 관련 설정
* 프로젝트 전체에서 import하여 사용

> 변경하면 전체 UI 스타일이 바뀌는 핵심 설정 모듈

---

## 🎨 11. style.py — **UI 스타일/테마 정의**

* ttk 위젯 스타일, 버튼 테마, 달력 셀 스타일 설정
* 라이트/다크모드 확장 가능

> UI의 외형을 담당

---

## 📜 12. __init__.py — **패키지 초기 설정**

* 외부에서 import할 수 있는 구성 정의
  예)

```python
from .ui_app import MintCalendarApp
```

> 패키지의 입구 역할

---

## 🗂️ 13. events.db — **SQLite 일정 저장 파일**

* 자동 생성되는 DB 파일
* 모든 일정 데이터가 저장되는 실제 저장소

---



