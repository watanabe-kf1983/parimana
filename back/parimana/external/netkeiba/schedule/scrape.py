from dataclasses import dataclass
import datetime
from typing import Sequence


from parimana.domain.schedule import ScheduleSource, RaceInfo, Fixture
from parimana.external.netkeiba.base import NetKeibaRace, category_keiba
from parimana.external.netkeiba.schedule.base import JraCourse
from parimana.external.netkeiba.schedule.browse import (
    browse_monthly_calendar,
    browse_schedule,
)
from parimana.external.netkeiba.schedule.extract import (
    RaceListItem,
    extract_open_days,
    extract_schedule,
)


@dataclass
class _KeibaScheduleSource(ScheduleSource):

    def scrape_day_schedule(self, date: datetime.date) -> Sequence[RaceInfo]:
        return _scrape_day_schedule(date)

    def scrape_calendar(self, year: int, month: int) -> Sequence[datetime.date]:
        return _scrape_calendar(year, month)


schedule_source = _KeibaScheduleSource()


def _scrape_day_schedule(date: datetime.date) -> Sequence[RaceInfo]:
    day_schedule_page = browse_schedule(date)
    return [_item_to_race(item, date) for item in extract_schedule(day_schedule_page)]


def _scrape_calendar(year: int, month: int) -> Sequence[datetime.date]:
    calendar_page = browse_monthly_calendar(year, month)
    return [datetime.date(year, month, day) for day in extract_open_days(calendar_page)]


def _item_to_race(item: RaceListItem, date: datetime.date) -> RaceInfo:
    print(item)
    return RaceInfo(
        race_id=NetKeibaRace(item.netkeiba_race_id).race_id,
        name=f"{item.race_num_text}",
        fixture=Fixture(
            course=JraCourse.from_code(code=item.keibajo_code).to_course(), date=date
        ),
        poll_closing_time=datetime.datetime.combine(
            date,
            (
                datetime.datetime.strptime(item.start_time_text, "%H:%M")
                + datetime.timedelta(minutes=-1)
            ).time(),
            category_keiba.timezone,
        ),
    )
