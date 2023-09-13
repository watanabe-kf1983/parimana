from typing import Mapping

from parimana.base.eye import Eye
from parimana.base.odds import Odds

from parimana.race.boatrace.browse import browse_odds_pages
from parimana.race.boatrace.extract import extract_odds


def collect_odds(date: str, cource: int, race_no: int) -> Mapping[Eye, Odds]:
    return {
        eye: odds
        for content, btype in browse_odds_pages(date, cource, race_no)
        for eye, odds in extract_odds(content, btype).items()
    }
