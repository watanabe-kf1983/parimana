from abc import ABC, abstractmethod
import datetime
from typing import Optional, Sequence

from parimana.app.exception import ResultNotExistError
from parimana.domain.schedule import Category, CategorySelector, RaceInfo


class ScheduleRepository(ABC):

    @abstractmethod
    def save_calendar(
        self,
        cat: Category,
        calendar: Sequence[datetime.date],
    ):
        pass

    @abstractmethod
    def load_calendar(self, cat: Category) -> Optional[Sequence[datetime.date]]:
        pass

    @abstractmethod
    def save_schedule(
        self,
        cat: Category,
        date: datetime.date,
        schedule: Sequence[RaceInfo],
    ):
        pass

    @abstractmethod
    def load_schedule(
        self, cat: Category, date: datetime.date
    ) -> Optional[Sequence[RaceInfo]]:
        pass

    @abstractmethod
    def save_race_info(self, race_info: RaceInfo):
        pass

    @abstractmethod
    def load_race_info(self, race_id: str) -> Optional[RaceInfo]:
        pass


class ScheduleApp:
    def __init__(self, categories: Sequence[Category], repo: ScheduleRepository):
        self.category_selector = CategorySelector(categories)
        self.repo: ScheduleRepository = repo

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
