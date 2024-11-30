from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence
from datetime import date


@dataclass
class Category:
    id: str
    name: str
    fixture_source: "FixtureSource"


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


class FixtureSource(ABC):
    @abstractmethod
    def scrape_calendar(
        self, date_from: Optional[date] = None, date_to: Optional[date] = None
    ) -> Mapping[date, Sequence[RaceSchedule]]:
        pass

    @abstractmethod
    def find_race_info(cls, race_id: str) -> Optional[RaceInfo]:
        pass
