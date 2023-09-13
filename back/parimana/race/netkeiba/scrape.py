from typing import Mapping

from parimana.base.eye import Eye
from parimana.base.odds import Odds
from parimana.race.netkeiba.browse import browse_odds_pages
from parimana.race.netkeiba.extract import extract_odds


def collect_odds(netkeiba_race_id: str) -> Mapping[Eye, Odds]:
    return {
        eye: odds
        for content, btype in browse_odds_pages(netkeiba_race_id)
        for eye, odds in extract_odds(content, btype).items()
    }
