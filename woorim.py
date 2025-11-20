#202062075 김우림 / serch
# search_module.py

def search_date(schedule_list, date):
    return [item for item in schedule_list if item["date"] == date]


def search_keyword(schedule_list, keyword):
    return [item for item in schedule_list if keyword.lower() in item["title"].lower()]


def search_student(schedule_list, student):
    return [item for item in schedule_list if student.lower() in item["student"].lower()]


    return result
