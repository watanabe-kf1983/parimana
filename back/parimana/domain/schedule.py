from abc import ABC, abstractmethod
from dataclasses import dataclass
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
    # poll_closing_time: datetime
    fixture: Fixture


class ScheduleSource(ABC):
    @abstractmethod
    def scrape_day_schedule(self, date: date) -> Sequence[RaceInfo]:
        pass

    @abstractmethod
    def scrape_calendar(self, year: int, month: int) -> Sequence[date]:
        pass
