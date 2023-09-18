from dataclasses import dataclass
from typing import Optional

from parimana.base import BettingType
from parimana.race.race import Race
from parimana.race.race_source import RaceSource
from parimana.race.odds_pool import RaceOddsPool
from parimana.race.netkeiba.race import NetKeibaRace
from parimana.race.netkeiba.scrape import collect_odds

# ratio_data = {
#     # https://jra.jp/company/about/financial/pdf/houkoku03.pdf p.26 別表9
#     BettingType.WIN: 6.9,
#     BettingType.QUINELLA: 13.3,
#     BettingType.EXACTA: 5.7,
#     BettingType.TRIO: 21.7,
#     BettingType.TRIFECTA: 29.0,
# }

ratio_data_derby = {
    # https://jra-van.jp/fun/baken/index3.html
    BettingType.WIN: 6.3,
    BettingType.QUINELLA: 16.3,
    BettingType.EXACTA: 6.3,
    BettingType.TRIO: 19.5,
    BettingType.TRIFECTA: 37.1,
}


@dataclass
class NetKeibaSource(RaceSource):
    nk_race: NetKeibaRace

    @property
    def race(self) -> Race:
        return self.nk_race

    def scrape_odds_pool(self) -> RaceOddsPool:
        odds, timestamp = collect_odds(self.nk_race)
        return RaceOddsPool(
            race=self.race,
            odds=odds,
            timestamp=timestamp,
            vote_ratio=ratio_data_derby,
        )

    @classmethod
    def from_race(cls, race: Race) -> Optional[RaceSource]:
        if isinstance(race, NetKeibaRace):
            return NetKeibaSource(race)
        else:
            return None
