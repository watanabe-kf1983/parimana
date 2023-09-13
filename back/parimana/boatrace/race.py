from dataclasses import dataclass
from typing import Mapping, Optional
import re

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.base.race import RaceOddsPool, RaceSource
from parimana.boatrace.browse import browse_odds_pages
from parimana.boatrace.extract import extract_odds

# https://funaban.com/wp/post-543.html
ratio_data = {
    BettingType.WIN: 0.0,
    BettingType.QUINELLA: 0.01,
    BettingType.EXACTA: 0.04,
    BettingType.TRIO: 0.03,
    BettingType.TRIFECTA: 0.92,
}

RACE_ID_PATTERN: re.Pattern = re.compile(
    r"boatrace-(?P<date>[0-9]{8})-(?P<cource>[0-9]{1,2})-(?P<race_no>[0-9]{1,2})"
)


@dataclass
class BoatRaceSource(RaceSource):
    date: str
    cource: int
    race_no: int

    @property
    def race_id(self) -> str:
        return f"boatrace-{self.date}-{self.cource}-{self.race_no}"

    def scrape_odds_pool(self) -> RaceOddsPool:
        return RaceOddsPool(
            race_id=self.race_id,
            vote_ratio=ratio_data,
            odds=self._collect_odds(),
        )

    def _collect_odds(self) -> Mapping[Eye, Odds]:
        return {
            eye: odds
            for content, btype in browse_odds_pages(
                self.date, self.cource, self.race_no
            )
            for eye, odds in extract_odds(content, btype).items()
        }

    @classmethod
    def from_race_id(cls, race_id: str) -> Optional["BoatRaceSource"]:
        if m := re.fullmatch(RACE_ID_PATTERN, race_id):
            dict = m.groupdict()
            return BoatRaceSource(
                date=dict["date"],
                cource=int(dict["cource"]),
                race_no=int(dict["race_no"]),
            )
        else:
            return None
