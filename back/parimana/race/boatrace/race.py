from dataclasses import dataclass
import datetime
import re
from typing import Optional

from parimana.race.base import Race, RaceSource


RACE_ID_PATTERN: re.Pattern = re.compile(
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
    def source(self) -> RaceSource:
        from parimana.race.boatrace.scrape import BoatRaceSource

        return BoatRaceSource(self)

    @classmethod
    def from_id(cls, race_id: str) -> Optional["BoatRace"]:

        if m := re.fullmatch(RACE_ID_PATTERN, race_id):
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
