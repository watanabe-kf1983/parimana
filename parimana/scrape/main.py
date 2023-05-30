from typing import Mapping

from parimana.base.eye import Eye
import parimana.scrape.netkeiba.main as netkeiba
from parimana.scrape.chrome import get_webdriver


def collect_odds(race_id: str) -> Mapping[Eye, float]:
    return netkeiba.collect_odds(get_webdriver(), race_id)
