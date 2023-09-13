from typing import Mapping, Tuple

from parimana.base.eye import Eye
from parimana.base.odds import Odds
from parimana.base.race import OddsTimeStamp, OddsUpdatedException

from parimana.race.boatrace.browse import browse_odds_pages
from parimana.race.boatrace.extract import extract_odds, extract_timestamp


def collect_odds(
    date: str, cource: int, race_no: int
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    try:
        return attempt_collect_odds(date, cource, race_no, "1st")

    except OddsUpdatedException:
        return attempt_collect_odds(date, cource, race_no, "2nd")


def attempt_collect_odds(
    date: str, cource: int, race_no: int, attempt: str
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    timestamp: OddsTimeStamp = None
    odds: Mapping[Eye, Odds] = {}

    for content, btype in browse_odds_pages(date, cource, race_no, attempt):
        ts = extract_timestamp(content)
        if timestamp is None:
            timestamp = ts
        else:
            if ts != timestamp:
                print("Odds update detected")
                raise OddsUpdatedException()

        odds |= extract_odds(content, btype)

    return odds, timestamp
