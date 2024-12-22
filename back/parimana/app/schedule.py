from typing import Optional, Sequence

from parimana.domain.schedule import Category, CategorySelector, RaceInfo
from parimana.io.kvs import Storage
from parimana.repository.schedule import ScheduleRepository, ScheduleRepositoryImpl
from parimana.app.exception import ResultNotExistError


class ScheduleApp:
    def __init__(self, categories: Sequence[Category], store: Storage):
        self.category_selector = CategorySelector(categories)
        self.repo: ScheduleRepository = ScheduleRepositoryImpl(store)

    def select_category(self, category_id: str):
        return self.category_selector.select(category_id)

    def get_schedule(
        self,
        cat: Category,
    ) -> Sequence[RaceInfo]:

        return [
            race_info
            for date in (self.repo.load_calendar(cat) or [])
            for race_info in (self.repo.load_schedule(cat, date) or [])
        ]

    def find_race(self, url: str) -> Optional[RaceInfo]:
        return None

    def get_race(self, race_id: str) -> RaceInfo:
        if race_info := self.repo.load_race_info(race_id):
            return race_info
        else:
            raise ResultNotExistError(f"{race_id} not found")

    def scrape_and_get_schedule(self, cat: Category) -> Sequence[RaceInfo]:

        source = cat.schedule_source
        repo = self.repo

        calendar = repo.load_calendar(cat)
        if not calendar:
            calendar = source.scrape_calendar()
            repo.save_calendar(cat=cat, calendar=calendar)

        all_schedule: Sequence[RaceInfo] = []

        for date in calendar:
            day_schedule = repo.load_schedule(cat, date)

            if day_schedule is None:
                day_schedule = source.scrape_day_schedule(date)
                repo.save_schedule(cat=cat, date=date, schedule=day_schedule)
                for race_info in day_schedule:
                    repo.save_race_info(race_info)

            all_schedule.extend(day_schedule)

        return all_schedule
