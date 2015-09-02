from datetime import datetime


def friendly_day(ugly_date):
    date = _parse_date(ugly_date)
    diff = datetime.now().date() - date

    if diff.days == 0:
        return "Today"
    elif diff.days == -1:
        return "Yesterday"
    else:
        return date.strftime("%A")


def _parse_date(ugly_date):
    return datetime.strptime(ugly_date, '%Y-%m-%dT%H:%M:%S.%f').date()


def friendly_date(ugly_date):
    date = _parse_date(ugly_date)
    return date.strftime('%d.%m.%y')
