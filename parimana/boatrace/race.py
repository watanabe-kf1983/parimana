from dataclasses import dataclass
from functools import cached_property
from typing import Mapping

from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
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


@dataclass(frozen=True)
class BoatRace(Race):
    date: str
    cource: int
    number: int

    @cached_property
    def contestants(self) -> Contestants:
        return Contestants.no_absences(6)

    @property
    def vote_ratio(self) -> Mapping[BettingType, float]:
        return ratio_data

    @property
    def vote_tally_total(self) -> float:
        return 100_000_000

    @property
    def race_id(self) -> str:
        return f"boat{self.date}-{self.cource}-{self.number}"

    def collect_odds(self) -> Mapping[Eye, float]:
        return {
            eye: odds
            for content, btype in browse_odds_pages(self.date, self.cource, self.number)
            for eye, odds in extract_odds(content, btype).items()
        }
