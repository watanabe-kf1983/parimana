from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from typing import Optional, Sequence

from parimana.domain.schedule import Category, RaceInfo
from parimana.io.kvs import Storage


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


@dataclass
class ScheduleRepositoryImpl(ScheduleRepository):
    store: Storage

    def save_calendar(
        self,
        cat: Category,
        calendar: Sequence[datetime.date],
    ):
        today = datetime.datetime.now(cat.timezone).strftime("%Y%m%d")
        self.store.write_object(
            f"schedule/cat/{cat.id}/calendar{today}_.pickle", calendar
        )

    def load_calendar(self, cat: Category) -> Optional[Sequence[datetime.date]]:
        today = datetime.datetime.now(cat.timezone).strftime("%Y%m%d")
        return self.store.read_object(f"schedule/cat/{cat.id}/calendar{today}_.pickle")

    def save_schedule(
        self,
        cat: Category,
        date: datetime.date,
        schedule: Sequence[RaceInfo],
    ):
        self.store.write_object(
            f"schedule/cat/{cat.id}/{date:%Y%m%d}_schedule.pickle", schedule
        )

    def load_schedule(
        self, cat: Category, date: datetime.date
    ) -> Optional[Sequence[RaceInfo]]:
        return self.store.read_object(
            f"schedule/cat/{cat.id}/{date:%Y%m%d}_schedule.pickle"
        )

    def save_race_info(self, race_info: RaceInfo):
        self.store.write_object(f"schedule/races/{race_info.race_id}.pickle", race_info)

    def load_race_info(self, race_id: str) -> Optional[RaceInfo]:
        return self.store.read_object(f"schedule/races/{race_id}.pickle")
