from dataclasses import dataclass
import re
from typing import Optional

from parimana.race.base import Race, RaceSource


@dataclass
class NetKeibaRace(Race):
    netkeiba_race_id: str

    @property
    def race_id(self) -> str:
        return f"netkeiba-{self.netkeiba_race_id}"

    @property
    def source(self) -> RaceSource:
        from parimana.race.netkeiba.scrape import NetKeibaSource

        return NetKeibaSource(self)

    @classmethod
    def from_id(cls, race_id: str) -> Optional[Race]:
        if m := re.fullmatch(RACE_ID_PATTERN, race_id):
            return NetKeibaRace(**m.groupdict())
        else:
            return None


RACE_ID_PATTERN: re.Pattern = re.compile(r"netkeiba-(?P<netkeiba_race_id>[0-9]{12})")
