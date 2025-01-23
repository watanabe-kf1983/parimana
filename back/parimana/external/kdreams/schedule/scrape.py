import calendar
import datetime
from typing import Sequence


from parimana.domain.schedule import ScheduleSource, RaceInfo
from parimana.external.kdreams.base import KeirinRace, category_keirin
import parimana.external.kdreams.schedule.browse as browser
import parimana.external.kdreams.schedule.extract as ext


class _KeirinScheduleSource(ScheduleSource):

    def scrape_day_schedule(self, date: datetime.date) -> Sequence[RaceInfo]:
        return [
            race
            for meeting_day_link in _scrape_meeting_day_link(date)
            for race in _scrape_schedule(meeting_day_link)
        ]

    def scrape_calendar(self, year: int, month: int) -> Sequence[datetime.date]:
        _, last_day = calendar.monthrange(year, month)
        return [datetime.date(year, month, day) for day in range(1, last_day + 1)]

    def scrape_race_info(self, race_id: str) -> RaceInfo:
        return _scrape_race_info(race_id)

    def site_name(self):
        return "kdreams.jp"


schedule_source = _KeirinScheduleSource()


def _scrape_meeting_day_link(date: datetime.date) -> Sequence[str]:
    idx_page = browser.browse_day_index(date)
    return ext.extract_meeting_day_link(idx_page)


def _scrape_schedule(meeting_day_link: str) -> Sequence[RaceInfo]:
    meeting_day_page = browser.browse_link(meeting_day_link)
    return [
        _to_race_info_from_ext(extracted)
        for extracted in ext.extract_races(meeting_day_page)
    ]


def _scrape_race_info(race_id: str) -> RaceInfo:
    race = KeirinRace.from_id(race_id)
    page = browser.browse_race(race)
    ext.extract_race_info(page)


def _to_race_info_from_ext(extracted: ext.ExtractedRaceInfo) -> RaceInfo:
    return _to_race_info(
        KeirinRace.from_uri(extracted.link), extracted.poll_closing_time
    )


def _to_race_info(race: KeirinRace, poll_closing_time: datetime.time) -> RaceInfo:
    return RaceInfo(
        race_id=race.race_id,
        name=race.name,
        fixture=race.meeting_day.to_fixture(),
        poll_closing_time=datetime.datetime.combine(
            race.meeting_day.date,
            poll_closing_time,
            category_keirin.timezone,
        ),
    )
