schedule = {}  

def add_schedule(date, content):
    # 해당 날짜가 처음 등록되는 경우
    if date not in schedule:
        schedule[date] = []
    
    # 일정 추가
    schedule[date].append(content)
    print(f"일정이 등록되었습니다: {date} - {content}")
