from dataclasses import dataclass
from typing import Optional
import re

from parimana.base.eye import BettingType
from parimana.base.race import RaceOddsPool, RaceSource, Race
from parimana.race.boatrace.scrape import collect_odds


@dataclass
class BoatRace(Race):
    date: str
    cource: int
    race_no: int

    @property
    def race_id(self) -> str:
        return f"boatrace-{self.date}-{self.cource}-{self.race_no}"

    @property
    def source(self) -> RaceSource:
        return BoatRaceSource(self)

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


@dataclass
class BoatRaceSource(RaceSource):
    race: BoatRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        race = self.race
        odds, timestamp = collect_odds(race.date, race.cource, race.race_no)
        return RaceOddsPool(
            race=race,
            odds=odds,
            timestamp=timestamp,
            vote_ratio=ratio_data,
        )


# https://funaban.com/wp/post-543.html
ratio_data = {
    BettingType.WIN: 0.0,
    BettingType.QUINELLA: 0.01,
    BettingType.EXACTA: 0.04,
    BettingType.TRIO: 0.03,
    BettingType.TRIFECTA: 0.92,
}
