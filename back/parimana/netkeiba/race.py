from dataclasses import dataclass
import re
from typing import Mapping, Optional

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.base.race import RaceOddsPool, RaceSource, Race
from parimana.netkeiba.browse import browse_odds_pages
from parimana.netkeiba.extract import extract_odds

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

RACE_ID_PATTERN: re.Pattern = re.compile(r"netkeiba-(?P<netkeiba_race_id>[0-9]{12})")


@dataclass
class NetKeibaRace(Race):
    netkeiba_race_id: str

    @property
    def race_id(self) -> str:
        return f"netkeiba-{self.netkeiba_race_id}"

    @property
    def source(self) -> RaceSource:
        return NetKeibaSource(self)

    @classmethod
    def from_id(cls, race_id: str) -> Optional[Race]:
        if m := re.fullmatch(RACE_ID_PATTERN, race_id):
            return NetKeibaRace(**m.groupdict())
        else:
            return None


@dataclass
class NetKeibaSource(RaceSource):
    race: NetKeibaRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        return RaceOddsPool(
            race=self.race,
            vote_ratio=ratio_data_derby,
            odds=self._collect_odds(),
        )

    def _collect_odds(self) -> Mapping[Eye, Odds]:
        return {
            eye: odds
            for content, btype in browse_odds_pages(self.race.netkeiba_race_id)
            for eye, odds in extract_odds(content, btype).items()
        }
