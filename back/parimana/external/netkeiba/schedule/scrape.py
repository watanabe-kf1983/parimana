import calendar
from dataclasses import dataclass
import datetime
from typing import Sequence, Type


from parimana.domain.schedule import Category, ScheduleSource, RaceInfo, Fixture
from parimana.external.netkeiba.base import (
    JraRace,
    NarRace,
    NetKeibaRace,
    category_jra,
    category_nar,
)
from parimana.external.netkeiba.schedule.base import (
    JraCourse,
    NarCourse,
    NetKeibaCourse,
)
from parimana.external.netkeiba.schedule.browse import (
    JraScheduleBrowser,
    NarScheduleBrowser,
)
from parimana.external.netkeiba.schedule.extract import (
    RaceListItem,
    JraScheduleExtractor,
    NarScheduleExtractor,
)


@dataclass
class JraScheduleSource(ScheduleSource):
    browser = JraScheduleBrowser()
    extractor = JraScheduleExtractor()

    def site_name(self):
        return self.browser.host_name

    def scrape_calendar(self, year: int, month: int) -> Sequence[datetime.date]:
        calendar_page = self.browser.browse_monthly_calendar(year, month)
        return [
            datetime.date(year, month, day)
            for day in self.extractor.extract_open_days(calendar_page)
        ]

    def scrape_day_schedule(self, date: datetime.date) -> Sequence[RaceInfo]:
        page = self.browser.browse_schedule(date)
        return [
            _item_to_race(
                item,
                date,
                category=category_jra,
                race_type=JraRace,
                cource_type=JraCourse,
            )
            for item in self.extractor.extract_schedule(page)
        ]

    def scrape_race_info(self, race_id: str) -> RaceInfo:
        race = JraRace.from_id(race_id)
        race_date = self.extractor.extract_race_date(self.browser.browse_race(race))
        schedule = self.scrape_day_schedule(race_date)
        for info in schedule:
            if info.race_id == race_id:
                return info

        raise Exception(f"race not found: {race_id}")


class NarScheduleSource:
    browser = NarScheduleBrowser()
    extractor = NarScheduleExtractor()

    def site_name(self):
        return self.browser.host_name

    def scrape_calendar(self, year: int, month: int) -> Sequence[datetime.date]:
        _, last_day = calendar.monthrange(year, month)
        return [datetime.date(year, month, day) for day in range(1, last_day + 1)]

    def scrape_day_schedule(self, date: datetime.date) -> Sequence[RaceInfo]:
        day_page = self.browser.browse_schedule_by_day(date)
        kaisai_ids = self.extractor.extract_schedule_kaisai_id(day_page)
        pages = [
            self.browser.browse_schedule_by_course(date, kaisai_id)
            for kaisai_id in kaisai_ids
        ]
        return [
            _item_to_race(
                item,
                date,
                category=category_nar,
                race_type=NarRace,
                cource_type=NarCourse,
            )
            for page in pages
            for item in self.extractor.extract_schedule(page)
        ]

    def scrape_race_info(self, race_id: str) -> RaceInfo:
        race = NarRace.from_id(race_id)
        if not race:
            raise ValueError(f"Illegal race id: {race_id}")
        page = self.browser.browse_schedule_by_course(
            date=race.date(), kaisai_id=race.kaisai_id()
        )
        items = self.extractor.extract_schedule(page)
        for item in items:
            ri: RaceInfo = _item_to_race(
                item,
                race.date(),
                category=category_nar,
                race_type=NarRace,
                cource_type=NarCourse,
            )
            if ri.race_id == race_id:
                return ri

        raise Exception(f"race not found: {race_id}")


def _item_to_race(
    item: RaceListItem,
    date: datetime.date,
    category: Category,
    race_type: Type[NetKeibaRace],
    cource_type: Type[NetKeibaCourse],
) -> RaceInfo:

    return RaceInfo(
        race_id=race_type(item.netkeiba_race_id).race_id,
        name=f"{item.race_num_text}",
        fixture=Fixture(
            course=cource_type.from_code(code=item.keibajo_code).to_course(),
            date=date,
        ),
        poll_closing_time=datetime.datetime.combine(
            date,
            (
                datetime.datetime.strptime(item.start_time_text, "%H:%M")
                + datetime.timedelta(minutes=-1)
            ).time(),
            category.timezone,
        ),
    )
