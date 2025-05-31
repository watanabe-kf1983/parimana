import datetime
from typing import Collection, Sequence

from parimana.domain.schedule import Category, CategorySelector, RaceInfo
from parimana.io.kvs import Storage
from parimana.repository.analysis import AnalysisRepository, AnalysisRepositoryImpl
from parimana.repository.schedule import ScheduleRepository, ScheduleRepositoryImpl
from parimana.app.exception import ResultNotExistError


class ScheduleApp:
    def __init__(self, category_selector: CategorySelector, store: Storage):
        self.category_selector = category_selector
        self.repo: ScheduleRepository = ScheduleRepositoryImpl(store)
        self.an_repo: AnalysisRepository = AnalysisRepositoryImpl(store)

    def get_today_schedule(
        self,
    ) -> Sequence[RaceInfo]:
        return [
            race_info
            for cat in self.category_selector.all()
            for race_info in (
                self.repo.load_schedule(cat, datetime.datetime.now(cat.timezone).date())
                or []
            )
        ]

    def get_recent_schedule(self) -> Sequence[RaceInfo]:
        return [
            race_info
            for cat in self.category_selector.all()
            for date in self.get_recent_calendar(cat)
            for race_info in (self.repo.load_schedule(cat, date) or [])
        ]

    def get_recent_calendar(
        self,
        cat: Category,
    ) -> Sequence[datetime.date]:

        calendar = self.repo.load_calendar(cat) or []
        today = datetime.datetime.now(cat.timezone).date()
        return [date for date in calendar if date <= today][-4:]

    def get_race(self, race_id: str) -> RaceInfo:
        if race_info := self.repo.load_race_info(race_id):
            return race_info
        else:
            raise ResultNotExistError(f"{race_id} not found")

    def scrape_race(self, cat: Category, race_id: str) -> RaceInfo:
        if race_info := self.repo.load_race_info(race_id):
            return race_info
        else:
            race_info = cat.schedule_source.scrape_race_info(race_id)
            self.repo.save_race_info(race_info)
            return race_info

    def update_calendar(self, cat: Category) -> None:

        today = datetime.datetime.now(cat.timezone).date()
        this_month = (today.year, today.month)

        calendar = self.repo.load_calendar(cat) or []
        if (not calendar) or this_month != (calendar[-1].year, calendar[-1].month):
            scraped = cat.schedule_source.scrape_calendar(*this_month)
            calendar = sorted(set(calendar + scraped))
            self.repo.save_calendar(cat, calendar)

    def update_schedule(self, cat: Category) -> None:

        self.update_calendar(cat)

        for date in self.get_recent_calendar(cat):
            self.update_day_schedule(cat, date)

    def update_day_schedule(
        self, cat: Category, date: datetime.date, scrape_force: bool = False
    ) -> None:

        if scrape_force or self.repo.load_schedule(cat, date) is None:
            day_schedule = cat.schedule_source.scrape_day_schedule(date)
            self.repo.save_schedule(cat=cat, date=date, schedule=day_schedule)
            for race_info in day_schedule:
                self.repo.save_race_info(race_info)

    def get_recent_analysed(self) -> Sequence[RaceInfo]:

        scheduled = self.get_recent_schedule()

        analysed = [
            race_info
            for cat, date in _distinct_cat_and_date(scheduled)
            for race_info in (self.repo.load_analysed(cat, date) or [])
        ]

        if not_analysed := set(scheduled) - set(analysed):
            new_analysed = self.an_repo.extract_charts_exist(list(not_analysed))
            analysed += new_analysed
            for cat, date in _distinct_cat_and_date(new_analysed):
                analysed_by_cat_date = [
                    race
                    for race in analysed
                    if race.fixture.course.category == cat and race.fixture.date == date
                ]
                self.repo.save_analysed(cat, date, analysed_by_cat_date)

        return analysed


def _distinct_cat_and_date(races: Collection[RaceInfo]):
    return {(ri.fixture.course.category, ri.fixture.date) for ri in races}
