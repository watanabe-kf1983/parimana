from datetime import datetime

import parimana.race.netkeiba.browser as browser


def browse_monthly_calendar(year: int, month: int) -> str:
    return browser.get(_monthly_calendar_page_uri(year, month))


def browse_schedule(date: datetime.date) -> str:
    return browser.get(_race_list_page_uri(date))


def _monthly_calendar_page_uri(year: int, month: int) -> str:
    return f"https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"


def _race_list_page_uri(date: datetime.date) -> str:
    return f"https://race.netkeiba.com/top/race_list.html?kaisai_date={date:%Y%m%d}"
