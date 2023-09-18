from typing import Mapping, Tuple

from parimana.base.eye import Eye
from parimana.base.odds import Odds
from parimana.base.odds_pool import OddsTimeStamp, OddsUpdatedException
from parimana.races.netkeiba.browse import browse_odds_pages
from parimana.races.netkeiba.extract import extract_odds, extract_timestamp
from parimana.races.netkeiba.race import NetKeibaRace


def collect_odds(race: NetKeibaRace) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    for attempt in ["1st", "2nd"]:
        try:
            return attempt_collect_odds(race)
        except OddsUpdatedException:
            pass


def attempt_collect_odds(
    race: NetKeibaRace,
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    timestamp: OddsTimeStamp = None
    odds: Mapping[Eye, Odds] = {}

    for content, btype in browse_odds_pages(race):
        ts = extract_timestamp(content)

        if timestamp is None:
            timestamp = ts

        if timestamp != ts:
            print("Odds update detected")
            raise OddsUpdatedException()

        odds |= extract_odds(content, btype)

    return odds, timestamp
