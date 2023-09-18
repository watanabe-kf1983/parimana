from typing import Mapping, Tuple

from parimana.base import Eye, Odds, OddsTimeStamp, OddsUpdatedException
from parimana.races.boatrace.race import BoatRace
from parimana.races.boatrace.browse import browse_odds_pages
from parimana.races.boatrace.extract import extract_odds, extract_timestamp


def collect_odds(race: BoatRace) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    for attempt in ["1st", "2nd"]:
        try:
            return attempt_collect_odds(race, attempt)
        except OddsUpdatedException:
            pass


def attempt_collect_odds(
    race: BoatRace, attempt: str
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    timestamp: OddsTimeStamp = None
    odds: Mapping[Eye, Odds] = {}

    for content, btype in browse_odds_pages(race, attempt):
        ts = extract_timestamp(content)

        if timestamp is None:
            timestamp = ts

        if timestamp != ts:
            print("Odds update detected")
            raise OddsUpdatedException()

        odds |= extract_odds(content, btype)

    return odds, timestamp
