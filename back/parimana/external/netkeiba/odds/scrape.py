from dataclasses import dataclass
from typing import Mapping, Tuple

from parimana.io.message import mprint
from parimana.domain.base import Eye, Odds
from parimana.domain.race import (
    OddsTimeStamp,
    OddsUpdatedException,
    RaceOddsPool,
    OddsSource,
)
from parimana.external.netkeiba.base import JraRace
from parimana.external.netkeiba.odds.data import ratio_data_derby
from parimana.external.netkeiba.odds.extract import extract_odds, extract_timestamp
from parimana.external.netkeiba.odds.browse import (
    browse_odds_pages,
    browse_for_odds_timestamp,
    get_source_uri,
)


@dataclass
class NkJraRaceSource(OddsSource):
    race: JraRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        return scrape_odds_pool(self.race)

    def scrape_timestamp(self) -> OddsTimeStamp:
        return scrape_timestamp(self.race)

    def get_uri(self) -> str:
        return get_source_uri(self.race)

    @classmethod
    def site_name(cls):
        return "race.netkeiba.com"


def scrape_odds_pool(race: JraRace) -> RaceOddsPool:
    odds, timestamp = collect_odds(race)
    return RaceOddsPool(
        race=race,
        odds=odds,
        timestamp=timestamp,
        vote_ratio=ratio_data_derby,
    )


def scrape_timestamp(race: JraRace) -> OddsTimeStamp:
    return extract_timestamp(browse_for_odds_timestamp(race))


def collect_odds(race: JraRace) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    for attempt in ["1st", "2nd"]:
        try:
            return attempt_collect_odds(race)
        except OddsUpdatedException:
            pass

    raise ValueError("collect_odds Failed")


def attempt_collect_odds(
    race: JraRace,
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    odds: dict[Eye, Odds] = {}
    timestamp = scrape_timestamp(race)

    for content, btype in browse_odds_pages(race):
        if extract_timestamp(content) != timestamp:
            mprint("Odds update detected")
            raise OddsUpdatedException()

        odds |= extract_odds(content, btype)

    return odds, timestamp
