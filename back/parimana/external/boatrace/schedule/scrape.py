import calendar
import datetime
from typing import Sequence


from parimana.domain.schedule import Fixture, ScheduleSource, RaceInfo
from parimana.external.boatrace.base import BoatRace, category_boat
from parimana.external.boatrace.schedule.base import BoatRaceJo
import parimana.external.boatrace.schedule.browse as browser
import parimana.external.boatrace.schedule.extract as ext


class _BoatScheduleSource(ScheduleSource):

    def scrape_day_schedule(self, date: datetime.date) -> Sequence[RaceInfo]:
        return [
            race for jo in _scrape_joes(date) for race in _scrape_schedule(date, jo)
        ]

    def scrape_calendar(self, year: int, month: int) -> Sequence[datetime.date]:
        _, last_day = calendar.monthrange(year, month)
        return [datetime.date(year, month, day) for day in range(1, last_day + 1)]


schedule_source = _BoatScheduleSource()


def _scrape_joes(date: datetime.date) -> Sequence[BoatRaceJo]:
    idx_page = browser.browse_day_index(date)
    return ext.extract_joes(idx_page)


def _scrape_schedule(date: datetime.date, boat_jo: BoatRaceJo) -> Sequence[RaceInfo]:
    fixture = Fixture(date=date, course=boat_jo.to_course())
    jo_page = browser.browse_schedule(date, boat_jo.jo_code)
    s_races = ext.extract_races(jo_page)
    return [
        RaceInfo(
            race_id=BoatRace(
                date=date, jo_code=boat_jo.jo_code, race_no=sr.race_no
            ).race_id,
            name=sr.name,
            fixture=fixture,
            poll_closing_time=datetime.datetime.combine(
                date, sr.poll_closing_time, category_boat.timezone
            ),
        )
        for sr in s_races
    ]
