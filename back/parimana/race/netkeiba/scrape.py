from typing import Mapping, Tuple, Optional

from parimana.base import Eye, Odds
from parimana.race.base import OddsTimeStamp, OddsUpdatedException
from parimana.race.netkeiba.browse import browse_odds_pages
from parimana.race.netkeiba.extract import extract_odds, extract_timestamp
from parimana.race.netkeiba.race import NetKeibaRace


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
    timestamp: Optional[OddsTimeStamp] = None
    odds: dict[Eye, Odds] = {}

    for content, btype in browse_odds_pages(race):
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
