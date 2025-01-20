from dataclasses import dataclass
from datetime import datetime

from parimana.external.netkeiba.base import JraRace
import parimana.external.netkeiba.browser as browser


@dataclass
class JraScheduleBrowser:
    host_name = "race.netkeiba.com"

    def browse_monthly_calendar(self, year: int, month: int) -> str:
        return browser.get(self._monthly_calendar_page_uri(year, month))

    def browse_schedule(self, date: datetime.date) -> str:
        return browser.get(self._race_list_page_uri(date))

    def browse_race(self, race: JraRace) -> str:
        return browser.get(self._race_page_uri(race))

    def _monthly_calendar_page_uri(self, year: int, month: int) -> str:
        return f"https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"

    def _race_list_page_uri(self, date: datetime.date) -> str:
        return f"https://race.netkeiba.com/top/race_list.html?kaisai_date={date:%Y%m%d}"

    def _race_page_uri(self, race: JraRace) -> str:
        return (
            f"https://race.netkeiba.com/race/shutuba.html"
            f"?race_id={race.netkeiba_race_id}"
        )


@dataclass
class NarScheduleBrowser:
    host_name = "nar.netkeiba.com"

    def browse_schedule_by_day(self, date: datetime.date) -> str:
        return browser.get(self._race_list_page_uri(date))

    def browse_schedule_by_course(self, date: datetime.date, kaisai_id: str) -> str:
        return browser.get(self._race_list_page_by_tab_uri(date, kaisai_id))

    def _race_list_page_uri(self, date: datetime.date) -> str:
        return f"https://nar.netkeiba.com/top/race_list.html?kaisai_date={date:%Y%m%d}"

    def _race_list_page_by_tab_uri(self, date: datetime.date, kaisai_id: str) -> str:
        return (
            f"https://nar.netkeiba.com/top/race_list.html?"
            f"kaisai_id={kaisai_id}&kaisai_date={date:%Y%m%d}"
        )
