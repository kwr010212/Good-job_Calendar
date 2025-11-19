# calendar_app/holidays.py
import datetime as dt

# 한국 공휴일 라이브러리 (없으면 기본 양력 공휴일만 사용)
try:
    from holidayskr import year_holidays
    HAS_HOLIDAYSKR = True
except ImportError:
    HAS_HOLIDAYSKR = False


def get_korean_holidays(year: int) -> dict:
    """
    해당 연도의 한국 공휴일을 dict[date, name] 형태로 반환.
    holidayskr가 설치돼 있으면 그걸 쓰고,
    아니면 기본적인 양력 공휴일만 사용.
    """
    holidays = {}

    def add(date_obj, name: str):
        holidays[date_obj] = name

    if HAS_HOLIDAYSKR:
        for day, name in year_holidays(str(year)):
            holidays[day] = name
        return holidays

    # 폴백: 기본 양력 공휴일만
    add(dt.date(year, 1, 1), "신정")
    add(dt.date(year, 3, 1), "삼일절")
    add(dt.date(year, 5, 5), "어린이날")
    add(dt.date(year, 6, 6), "현충일")
    add(dt.date(year, 8, 15), "광복절")
    add(dt.date(year, 10, 3), "개천절")
    add(dt.date(year, 10, 9), "한글날")
    add(dt.date(year, 12, 25), "성탄절")
    return holidays
