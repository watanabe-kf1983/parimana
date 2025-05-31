from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from typing import Sequence, Type
from datetime import date, timedelta
from zoneinfo import ZoneInfo

from parimana.domain.race import Race


@dataclass(frozen=True)
class Category(ABC):
    id: str
    name: str
    timezone: ZoneInfo
    race_type: Type[Race]
    poll_start_time: datetime.time

    @property
    @abstractmethod
    def schedule_source(self) -> "ScheduleSource":
        pass

    def contains(self, race: Race) -> bool:
        return isinstance(race, self.race_type)


@dataclass
class CategorySelector:
    categories: Sequence[Category]

    def all(self) -> Sequence[Category]:
        return self.categories

    def select(self, category_id: str) -> Category:
        for category in self.all():
            if category.id == category_id:
                return category

        raise ValueError(f"category_id: {category_id} is illegal")

    def select_from_race(self, race: Race) -> Category:
        for category in self.all():
            if category.contains(race):
                return category

        raise ValueError(f"category not found: {race}")

    def source_sites(self) -> Sequence[str]:
        return [category.schedule_source.site_name() for category in self.categories]


@dataclass(frozen=True)
class Course:
    id: str
    name: str
    category: Category


@dataclass(frozen=True)
class Fixture:
    """
    開催日
    """

    course: Course
    date: date


@dataclass(frozen=True)
class RaceInfo:
    race_id: str
    name: str
    fixture: Fixture
    poll_closing_time: datetime.datetime

    @property
    def poll_start_time(self) -> datetime.datetime:
        return datetime.datetime.combine(
            self.poll_closing_time.date(),
            self.fixture.course.category.poll_start_time,
            self.fixture.course.category.timezone,
        )

    def generate_analyse_schedule(
        self,
        closing_time_delta_list: Sequence[int],
        time_from: datetime.datetime,
        time_to: datetime.datetime,
    ) -> Sequence[datetime.datetime]:

        return [
            t
            for t in set(
                max(
                    self.poll_start_time,
                    (self.poll_closing_time + timedelta(minutes=delta_min)),
                )
                for delta_min in closing_time_delta_list
            )
            if time_from < t < time_to
        ]


class ScheduleSource(ABC):
    @abstractmethod
    def scrape_race_info(self, race_id: str) -> RaceInfo:
        pass

    @abstractmethod
    def scrape_day_schedule(self, date: date) -> Sequence[RaceInfo]:
        pass

    @abstractmethod
    def scrape_calendar(self, year: int, month: int) -> Sequence[date]:
        pass

    @abstractmethod
    def site_name(self) -> str:
        pass
