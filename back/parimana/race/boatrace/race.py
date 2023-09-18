from dataclasses import dataclass
from typing import Optional
import re

from parimana.race.race import Race


@dataclass
class BoatRace(Race):
    date: str
    cource: int
    race_no: int

    @property
    def race_id(self) -> str:
        return f"boatrace-{self.date}-{self.cource}-{self.race_no}"

    @classmethod
    def from_id(cls, race_id: str) -> Optional[Race]:
        if m := re.fullmatch(RACE_ID_PATTERN, race_id):
            dict = m.groupdict()
            return BoatRace(
                date=dict["date"],
                cource=int(dict["cource"]),
                race_no=int(dict["race_no"]),
            )
        else:
            return None


RACE_ID_PATTERN: re.Pattern = re.compile(
    r"boatrace-(?P<date>[0-9]{8})-(?P<cource>[0-9]{1,2})-(?P<race_no>[0-9]{1,2})"
)
