import datetime
from pathlib import Path
from typing import Optional, Sequence


from parimana.domain.schedule import Category, RaceInfo
from parimana.app.schedule import ScheduleRepository
from parimana.devices.file.repository.base import FileRepositoryBase
import parimana.devices.file.repository.utils as utils


class FileScheduleRepository(FileRepositoryBase, ScheduleRepository):

    def save_calendar(
        self,
        cat: Category,
        calendar: Sequence[datetime.date],
    ):
        dir_ = self._cat_dir(cat)
        utils.write_as_pickle(
            dir_
            / f"calendar{datetime.datetime.now(cat.timezone).date():%Y%m%d}.pickle",
            calendar,
        )

    def load_calendar(self, cat: Category) -> Optional[Sequence[datetime.date]]:
        dir_ = self._cat_dir(cat)
        return utils.read_pickle(
            dir_ / f"calendar{datetime.datetime.now(cat.timezone).date():%Y%m%d}.pickle"
        )

    def save_schedule(
        self,
        cat: Category,
        date: datetime.date,
        schedule: Sequence[RaceInfo],
    ):
        dir_ = self._cat_dir(cat)
        utils.write_as_pickle(dir_ / f"{date:%Y%m%d}_schedule.pickle", schedule)

    def load_schedule(
        self, cat: Category, date: datetime.date
    ) -> Optional[Sequence[RaceInfo]]:
        dir_ = self._cat_dir(cat)
        return utils.read_pickle(dir_ / f"{date:%Y%m%d}_schedule.pickle")

    def save_race_info(self, race_info: RaceInfo):
        utils.write_as_pickle(
            self._schedule_race_dir() / f"{race_info.race_id}.pickle",
            race_info,
        )

    def load_race_info(self, race_id: str) -> Optional[RaceInfo]:
        return utils.read_pickle(
            self._schedule_race_dir() / f"{race_id}.pickle",
        )

    def _cat_dir(self, cat: Category) -> Path:
        dir_ = self.root_path / "schedule" / "cat" / cat.id
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_

    def _schedule_race_dir(self) -> Path:
        dir_ = self.root_path / "schedule" / "races"
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_
