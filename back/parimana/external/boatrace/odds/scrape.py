from dataclasses import dataclass
from typing import Mapping, Tuple

from parimana.infra.message import mprint
from parimana.domain.base import Eye, Odds
from parimana.domain.race import (
    OddsTimeStamp,
    OddsUpdatedException,
    RaceOddsPool,
    OddsSource,
)

from parimana.external.boatrace.base import BoatRace
from parimana.external.boatrace.odds.data import ratio_data
from parimana.external.boatrace.odds.browse import (
    browse_odds_pages,
    browse_for_timestamp,
    get_source_uri,
)
from parimana.external.boatrace.odds.extract import extract_odds, extract_timestamp


@dataclass
class BoatRaceSource(OddsSource):
    race: BoatRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        return scrape_odds_pool(self.race)

    def scrape_timestamp(self) -> OddsTimeStamp:
        return scrape_timestamp(self.race)

    def get_uri(self) -> str:
        return get_source_uri(self.race)


def scrape_odds_pool(race: BoatRace) -> RaceOddsPool:
    odds, timestamp = collect_odds(race)
    return RaceOddsPool(
        race=race,
        odds=odds,
        timestamp=timestamp,
        vote_ratio=ratio_data,
    )


def scrape_timestamp(race: BoatRace) -> OddsTimeStamp:
    return extract_timestamp(browse_for_timestamp(race))


def collect_odds(race: BoatRace) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    for attempt in ["1st", "2nd"]:
        try:
            return attempt_collect_odds(race, attempt)
        except OddsUpdatedException:
            pass
    raise ValueError("collect_odds failed")


def attempt_collect_odds(
    race: BoatRace, attempt: str
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    odds: dict[Eye, Odds] = {}
    timestamp = scrape_timestamp(race)

    for content, btype in browse_odds_pages(race, attempt):
        if extract_timestamp(content) != timestamp:
            mprint("Odds update detected")
            raise OddsUpdatedException()

        odds |= extract_odds(content, btype)

    return odds, timestamp
