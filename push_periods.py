from datetime import datetime, timedelta


def push_periods(starts_at, days):
    periods = []
    a_day = timedelta(days=1)
    i = 1
    new_date = starts_at

    while i <= days:
        periods.append(new_date.strftime("%Y-%m-%d"))
        new_date = new_date + a_day
        i = i + 1
    return periods