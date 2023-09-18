from typing import Mapping, Tuple, Optional

from parimana.base import Eye, Odds
from parimana.race.odds_pool import OddsTimeStamp, OddsUpdatedException
from parimana.race.boatrace.race import BoatRace
from parimana.race.boatrace.browse import browse_odds_pages
from parimana.race.boatrace.extract import extract_odds, extract_timestamp


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
    timestamp: Optional[OddsTimeStamp] = None
    odds: dict[Eye, Odds] = {}

    for content, btype in browse_odds_pages(race, attempt):
        ts = extract_timestamp(content)

        if timestamp is None:
            timestamp = ts

        if timestamp != ts:
            print("Odds update detected")
            raise OddsUpdatedException()

        odds |= extract_odds(content, btype)

    if timestamp:
        return odds, timestamp
    else:
        raise ValueError("failed")
