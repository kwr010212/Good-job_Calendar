FILENAME = "schedule.txt"

def save_schedule(date, time, memo):
    try:
        with open(FILENAME, "a", encoding="utf-8") as f:
            f.write(date + " " + time + " " + memo + "\n")
    except Exception as e:
        print("오류 발생 다시 입력해주세요:", e)

def load_schedule():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            data = [line.strip() for line in f.readlines()]
        return data
    except:
        return 