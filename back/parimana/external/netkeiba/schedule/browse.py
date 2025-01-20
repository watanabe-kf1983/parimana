from datetime import datetime

from parimana.external.netkeiba.base import JraRace
import parimana.external.netkeiba.browser as browser


def browse_monthly_calendar(year: int, month: int) -> str:
    return browser.get(_monthly_calendar_page_uri(year, month))


def browse_schedule(date: datetime.date) -> str:
    return browser.get(_race_list_page_uri(date))


def browse_race(race: JraRace) -> str:
    return browser.get(_race_page_uri(race))


def _monthly_calendar_page_uri(year: int, month: int) -> str:
    return f"https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"


def _race_list_page_uri(date: datetime.date) -> str:
    return f"https://race.netkeiba.com/top/race_list.html?kaisai_date={date:%Y%m%d}"


def _race_page_uri(race: JraRace) -> str:
    return (
        f"https://race.netkeiba.com/race/shutuba.html?race_id={race.netkeiba_race_id}"
    )
