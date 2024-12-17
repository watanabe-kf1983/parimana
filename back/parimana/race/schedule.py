from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence
from datetime import date


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

    category: Category
    course: Course
    date: date


@dataclass
class RaceInfo:
    race_id: str
    name: str
    # poll_closing_time: datetime
    fixture: Fixture


@dataclass
class RaceSchedule:
    fixture: Fixture
    races: Sequence[RaceInfo]


class ScheduleSource(ABC):
    @abstractmethod
    def scrape(
        self, date_from: Optional[date] = None, date_to: Optional[date] = None
    ) -> Mapping[date, Sequence[RaceSchedule]]:
        pass

    @abstractmethod
    def find_race_info(cls, race_id: str) -> Optional[RaceInfo]:
        pass
