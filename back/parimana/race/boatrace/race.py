from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from parimana.race.base import Race, RaceSource
from parimana.race.boatrace.race_id import RaceIdElements


@dataclass
class BoatRace(Race):
    date: str
    cource: int
    race_no: int

    @property
    def race_id(self) -> str:
        return RaceIdElements(
            date=datetime.strptime(self.date, "%Y%m%d").date(),
            course_id=self.cource,
            race_no=self.race_no,
        ).generate_id()

    @property
    def source(self) -> RaceSource:
        from parimana.race.boatrace.scrape import BoatRaceSource

        return BoatRaceSource(self)

    @classmethod
    def from_id(cls, race_id: str) -> Optional[Race]:

        if elements := RaceIdElements.parse_from_id(race_id):
            return BoatRace(
                date=elements.date.strftime("%Y%m%d"),
                cource=elements.course_id,
                race_no=elements.race_no,
            )

        else:
            return None
