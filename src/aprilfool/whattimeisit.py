from datetime import datetime

# 获取当前时间
now = datetime.now()

# 分别提取 年、月、日
year: int = now.year
month: int = now.month
day: int = now.day

def update_date() -> None:
    global year, month, day
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day