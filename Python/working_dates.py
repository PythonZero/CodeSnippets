import datetime
import math
from typing import List
import workdays
from dateutil.relativedelta import relativedelta
import holidays


def _get_england_holidays(start_date, number_of_days: int):
    end_year = (
            start_date + relativedelta(years=math.ceil((number_of_days / 365) + 1))
    ).year
    uk_holidays = holidays.England(years=range(start_date.year, end_year)).keys()
    uk_holidays = [datetime.datetime(d.year, d.month, d.day) for d in uk_holidays]
    return uk_holidays


def get_working_days_in_month(start_date: datetime.datetime, number_of_months=12):
    """Gets the working days in a month for each month from the
    start date + the next n months

    :param start_date: start date
    :param number_of_months: number of months
    :return: dict of {start_date: working days in that month}
    """
    working_days = {}
    number_of_days = number_of_months * 365 / 12
    holidays = _get_england_holidays(start_date, number_of_days)
    for month_num in range(1, number_of_months + 1):
        end_date = start_date + relativedelta(months=1)
        num_working_days = workdays.networkdays(
            start_date, end_date + relativedelta(days=-1), holidays
        )
        working_days[start_date.date()] = num_working_days
        start_date = end_date
    return working_days


def get_working_days_between_dates(
        start_date: datetime.datetime, end_date: datetime.datetime
) -> List[datetime.date]:
    """Gets a list of working days between two dates

    :param start_date: start date
    :param end_date: end date
    :return: list of dates that are working days
    """
    num_days = (end_date - start_date).days
    holidays = _get_england_holidays(start_date, num_days)
    working_days = []
    for day_increment in range(num_days + 1):
        day = start_date + relativedelta(days=day_increment)
        is_workday = workdays.networkdays(day, day, holidays)
        if is_workday:
            working_days.append(day.date())
    return working_days



def test_get_working_days_in_month():
    expected_working_days = {
        datetime.date(2021, 6, 1): 22,
        datetime.date(2021, 7, 1): 22,
        datetime.date(2021, 8, 1): 21,
        datetime.date(2021, 9, 1): 22,
        datetime.date(2021, 10, 1): 21,
        datetime.date(2021, 11, 1): 22,
        datetime.date(2021, 12, 1): 21,
        datetime.date(2022, 1, 1): 20,
        datetime.date(2022, 2, 1): 20,
        datetime.date(2022, 3, 1): 23,
        datetime.date(2022, 4, 1): 19,
        datetime.date(2022, 5, 1): 20,
    }

    assert expected_working_days == get_working_days_in_month(
        datetime.datetime(2021, 6, 1), 12
    )


def test_get_working_days_between_dates():
    expected_working_days = [
        datetime.date(2021, 6, 1),
        datetime.date(2021, 6, 2),
        datetime.date(2021, 6, 3),
        datetime.date(2021, 6, 4),
        datetime.date(2021, 6, 7),
        datetime.date(2021, 6, 8),
        datetime.date(2021, 6, 9),
        datetime.date(2021, 6, 10),
        datetime.date(2021, 6, 11),
        datetime.date(2021, 6, 14),
        datetime.date(2021, 6, 15),
        datetime.date(2021, 6, 16),
        datetime.date(2021, 6, 17),
        datetime.date(2021, 6, 18),
        datetime.date(2021, 6, 21),
        datetime.date(2021, 6, 22),
        datetime.date(2021, 6, 23),
        datetime.date(2021, 6, 24),
        datetime.date(2021, 6, 25),
        datetime.date(2021, 6, 28),
        datetime.date(2021, 6, 29),
        datetime.date(2021, 6, 30),
    ]
    assert expected_working_days == get_working_days_between_dates(
        datetime.datetime(2021, 6, 1), datetime.datetime(2021, 6, 30)
    )
    assert len(expected_working_days) == 22

