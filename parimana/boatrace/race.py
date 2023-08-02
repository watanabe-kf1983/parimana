from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar, Mapping, Optional
import re

from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.base.race import Race
from parimana.boatrace.browse import browse_odds_pages
from parimana.boatrace.extract import extract_odds

ratio_data = {
    BettingType.WIN: 0.0,
    BettingType.QUINELLA: 0.0,
    BettingType.EXACTA: 0.0,
    BettingType.TRIO: 0.0,
    BettingType.TRIFECTA: 1.0,
}

vote_total = 100_000_000


@dataclass
class BoatRace(Race):
    date: str
    cource: int
    race_no: int

    @cached_property
    def contestants(self) -> Contestants:
        return Contestants.no_absences(6)

    @property
    def vote_ratio(self) -> Mapping[BettingType, float]:
        return ratio_data

    @property
    def race_id(self) -> str:
        return f"boatrace-{self.date}-{self.cource}-{self.race_no}"

    def collect_odds(self) -> Mapping[Eye, Odds]:
        return {
            eye: odds
            for content, btype in browse_odds_pages(
                self.date, self.cource, self.race_no
            )
            for eye, odds in extract_odds(content, btype).items()
        }

    PATTERN: ClassVar[str] = re.compile(
        r"boatrace-(?P<date>[0-9]{8})-(?P<cource>[0-9]{1,2})-(?P<race_no>[0-9]{1,2})"
    )

    @classmethod
    def from_race_id(cls, race_id: str) -> Optional["BoatRace"]:
        if m := re.fullmatch(cls.PATTERN, race_id):
            dict = m.groupdict()
            return BoatRace(
                date=dict["date"],
                cource=int(dict["cource"]),
                race_no=int(dict["race_no"]),
            )
        else:
            return None
