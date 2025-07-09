import calendar
import datetime
import traceback
from typing import Sequence


from parimana.domain.schedule import Fixture, ScheduleSource, RaceInfo
from parimana.external.autorace.base import (
    AutoRace,
    MotoStudium,
    category_moto,
    all_studiums,
)
import parimana.external.autorace.browser as browser
import parimana.external.autorace.schedule.extract as ext


class _MotoScheduleSource(ScheduleSource):

    def scrape_day_schedule(self, date: datetime.date) -> Sequence[RaceInfo]:
        return [
            race_info
            for studium in all_studiums
            for race_info in _scrape_schedule(date, studium)
        ]

    def scrape_calendar(self, year: int, month: int) -> Sequence[datetime.date]:
        _, last_day = calendar.monthrange(year, month)
        return [datetime.date(year, month, day) for day in range(1, last_day + 1)]

    def scrape_race_info(self, race_id: str) -> RaceInfo:
        return _scrape_race_info(AutoRace.from_id(race_id))

    def site_name(self):
        return "autorace.jp"


schedule_source = _MotoScheduleSource()


def _scrape_schedule(date: datetime.date, studium: MotoStudium) -> Sequence[RaceInfo]:

    schedule = []
    for race_no in range(1, 12 + 1):
        race = AutoRace(date=date, studium=studium, race_no=race_no)
        try:
            race_info = _scrape_race_info(race)
            schedule.append(race_info)

        except browser.NoContentError:
            break

        except Exception:
            print(f"Warning: skipped race_no {race_no}")
            print(traceback.format_exc())

    return schedule


def _scrape_race_info(race: AutoRace) -> RaceInfo:
    page = browser.browse_race_info_page(race)
    c_time = ext.extract_closing_time(page)
    return _to_race_info(race, c_time)


def _to_race_info(race: AutoRace, poll_closing_time: datetime.timedelta) -> RaceInfo:
    return RaceInfo(
        race_id=race.race_id,
        name=race.name,
        fixture=Fixture(course=race.studium.to_course(), date=race.date),
        poll_closing_time=(
            datetime.datetime.combine(
                race.date,
                datetime.time(0, 0, 0),
                category_moto.timezone,
            )
            + poll_closing_time
        ),
    )
