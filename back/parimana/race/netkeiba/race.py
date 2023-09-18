from dataclasses import dataclass
import re
from typing import Optional

from parimana.race.base import Race, RaceSource, RaceOddsPool


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


RACE_ID_PATTERN: re.Pattern = re.compile(r"netkeiba-(?P<netkeiba_race_id>[0-9]{12})")


@dataclass
class NetKeibaSource(RaceSource):
    race: NetKeibaRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        import parimana.race.netkeiba.scrape as scraper

        return scraper.scrape_odds_pool(self.race)
