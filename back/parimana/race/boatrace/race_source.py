from dataclasses import dataclass
from typing import Optional

from parimana.base.eye import BettingType
from parimana.base.odds_pool import RaceOddsPool
from parimana.base.race import Race
from parimana.base.race_source import RaceSource
from parimana.race.boatrace.race import BoatRace
from parimana.race.boatrace.scrape import collect_odds

# https://funaban.com/wp/post-543.html
ratio_data = {
    BettingType.WIN: 0.0,
    BettingType.QUINELLA: 0.01,
    BettingType.EXACTA: 0.04,
    BettingType.TRIO: 0.03,
    BettingType.TRIFECTA: 0.92,
}


@dataclass
class BoatRaceSource(RaceSource):
    boatrace: BoatRace

    @property
    def race(self) -> Race:
        return self.boatrace

    def scrape_odds_pool(self) -> RaceOddsPool:
        odds, timestamp = collect_odds(self.boatrace)
        return RaceOddsPool(
            race=self.boatrace,
            odds=odds,
            timestamp=timestamp,
            vote_ratio=ratio_data,
        )

    @classmethod
    def from_race(cls, race: Race) -> Optional[RaceSource]:
        if isinstance(race, BoatRace):
            return BoatRaceSource(race)
        else:
            return None
