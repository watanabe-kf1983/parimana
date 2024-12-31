from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from typing import Sequence
from datetime import date
from zoneinfo import ZoneInfo


@dataclass
class Category(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def schedule_source(self) -> "ScheduleSource":
        pass

    @property
    @abstractmethod
    def timezone(self) -> ZoneInfo:
        pass

    @property
    @abstractmethod
    def poll_start_time(self) -> datetime.time:
        pass


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

    def source_sites(self) -> Sequence[str]:
        return [category.schedule_source.site_name() for category in self.categories]


@dataclass
class Course:
    id: str
    name: str
    category: Category


@dataclass
class Fixture:
    """
    開催日
    """

    course: Course
    date: date


@dataclass
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


class ScheduleSource(ABC):
    @abstractmethod
    def scrape_day_schedule(self, date: date) -> Sequence[RaceInfo]:
        pass

    @abstractmethod
    def scrape_calendar(self, year: int, month: int) -> Sequence[date]:
        pass

    @abstractmethod
    def site_name(self) -> str:
        pass
