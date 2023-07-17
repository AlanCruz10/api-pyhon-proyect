import datetime


def format_date_now():
    now = datetime.datetime.now()
    second = now.second
    minute = now.minute
    hour = now.hour
    day = now.day
    month = now.month
    year = now.year
    format_time = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(day, month, year, hour, minute, second)
    return format_time
