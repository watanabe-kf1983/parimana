from dataclasses import dataclass
from typing import Mapping, Tuple

from parimana.base import Eye, Odds
from parimana.race.base import (
    OddsTimeStamp,
    OddsUpdatedException,
    RaceOddsPool,
    RaceSource,
)
from parimana.race.netkeiba.data import ratio_data_derby
from parimana.race.netkeiba.browse import browse_odds_pages, browse_for_odds_timestamp
from parimana.race.netkeiba.extract import extract_odds, extract_timestamp
from parimana.race.netkeiba.race import NetKeibaRace


@dataclass
class NetKeibaSource(RaceSource):
    race: NetKeibaRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        return scrape_odds_pool(self.race)

    def scrape_odds_timestamp(self) -> OddsTimeStamp:
        return scrape_odds_timestamp(self.race)


def scrape_odds_pool(race: NetKeibaRace) -> RaceOddsPool:
    odds, timestamp = collect_odds(race)
    return RaceOddsPool(
        race=race,
        odds=odds,
        timestamp=timestamp,
        vote_ratio=ratio_data_derby,
    )


def scrape_odds_timestamp(race: NetKeibaRace) -> OddsTimeStamp:
    return extract_timestamp(browse_for_odds_timestamp(race))


def collect_odds(race: NetKeibaRace) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    for attempt in ["1st", "2nd"]:
        try:
            return attempt_collect_odds(race)
        except OddsUpdatedException:
            pass

    raise ValueError("collect_odds Failed")


def attempt_collect_odds(
    race: NetKeibaRace,
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    odds: dict[Eye, Odds] = {}
    timestamp = scrape_odds_timestamp(race)

    for content, btype in browse_odds_pages(race):
        if extract_timestamp(content) != timestamp:
            print("Odds update detected")
            raise OddsUpdatedException()

        odds |= extract_odds(content, btype)

    return odds, timestamp
