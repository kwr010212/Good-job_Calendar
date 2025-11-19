
# 📘 **Mint Schedule Calendar**

Python + Tkinter 기반 일정 관리 프로그램
 데스크톱 달력입니다.

---

# 🚀 **How to Run**

## 1️⃣ 필요한 패키지 설치

```
pip install -r requirements.txt
```

또는 개별 설치:

```
pip install tkcalendar==1.6.1
pip install holidayskr==0.2.0
pip install korean-lunar-calendar==0.3.1
pip install babel==2.17.0
```

## 2️⃣ 실행

```
python run_calendar.py
```

프로그램이 실행되며 달력 UI가 나타납니다.

---

# 📦 **Requirements**

프로젝트 실행에 필요한 외부 패키지 목록입니다.

```
tkcalendar==1.6.1
holidayskr==0.2.0
korean-lunar-calendar==0.3.1
babel==2.17.0
```

---

# 📂 **Project Structure**

```
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
requirements.txt
README.md
```

---

# 🧩 **Module Overview (모듈 설명)**

각 파일은 단일 기능만 담당하도록 분리되어 있어
유지보수, 팀 협업, 기능 확장에 매우 유리한 구조로 되어 있습니다.

---

## 🎛️ ui_app.py — **전체 앱 조립**

* 메인 프로그램 구조 조립
* TopBar / CalendarView / StatusBar 배치
* 날짜창, 검색창, 월별 리스트창 호출

---

## 📅 calendar_view.py — **달력 화면**

* 달력 렌더링
* 이전/다음달 이동
* 공휴일 색칠
* 일정 있는 날짜 하이라이트
* 날짜 더블클릭 → 일정창 열기

---

## 🗓️ day_window.py — **날짜별 일정 관리**

* 일정 추가 / 수정 / 삭제
* 시간 선택 / 메모 / 카테고리
* 일정 변경 시 달력 하이라이트 갱신

---

## 📋 month_list.py — **이번 달 전체 일정 보기**

* 월 전체 일정 목록 보기
* 더블클릭 → 해당 날짜의 DayWindow

---

## 🔍 search_window.py — **일정 검색**

* 제목/내용 검색
* 검색 결과 목록
* 더블클릭 → 해당 날짜로 이동

---

## 🎚️ top_bar.py — **상단 메뉴 UI**

* 앱 제목
* 오늘 버튼 / 이번달 버튼 / 검색 버튼

---

## 📢 status_bar.py — **하단 상태창**

* 팁/안내 문구 제공

---

## 🎌 holidays.py — **한국 공휴일 계산**

* 연도별 공휴일 자동 생성
* 달력에 표시

---

## 🗃️ db.py — **SQLite 일정 저장소**

* events.db 관리
* CRUD 및 검색 기능 제공

---

## ⚙️ config.py — **공용 설정값**

* 글꼴 / 테마 색상 정의

---

## 🎨 style.py — **UI 스타일**

* ttk 위젯 스타일
* 셀 디자인
* 테마 관리

---

## 📜 **init**.py — **패키지 설정**

* import 경로 관리
  예)

```python
from .ui_app import MintCalendarApp
```








