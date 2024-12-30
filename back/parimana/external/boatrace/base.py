from dataclasses import dataclass
import datetime
import re
from typing import Optional, Type
from zoneinfo import ZoneInfo

from parimana.domain.race import Race, OddsSource
from parimana.domain.schedule import Category, ScheduleSource

_boat_timezone = ZoneInfo("Asia/Tokyo")


class _CategoryBoatRace(Category):
    @property
    def id(self) -> str:
        return "bt"

    @property
    def name(self) -> str:
        return "ボートレース"

    @property
    def schedule_source(self) -> ScheduleSource:
        from parimana.external.boatrace.schedule.scrape import schedule_source

        return schedule_source

    @property
    def timezone(self) -> ZoneInfo:
        return _boat_timezone


category_boat = _CategoryBoatRace()

_RACE_ID_PATTERN: re.Pattern = re.compile(
    r"bt(?P<date>[0-9]{8})(?P<jo_code>[0-9]{2})(?P<race_no>[0-9]{2})"
)


@dataclass
class BoatRace(Race):
    date: datetime.date
    jo_code: str
    race_no: int

    @property
    def race_id(self) -> str:
        return f"bt{self.date:%Y%m%d}{self.jo_code}{self.race_no:02}"

    @property
    def odds_source(self) -> OddsSource:
        return self.__class__.odds_source_type()(self)

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        from parimana.external.boatrace.odds.scrape import BoatRaceSource

        return BoatRaceSource

    @classmethod
    def from_id(cls, race_id: str) -> Optional["BoatRace"]:

        if m := re.fullmatch(_RACE_ID_PATTERN, race_id):
            parsed = m.groupdict()
            try:
                return cls(
                    date=datetime.datetime.strptime(parsed["date"], "%Y%m%d").date(),
                    jo_code=parsed["jo_code"],
                    race_no=int(parsed["race_no"]),
                )
            except Exception:
                return None

        else:
            return None
