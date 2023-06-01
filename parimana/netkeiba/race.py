from dataclasses import dataclass
from functools import cached_property
from typing import Mapping

from selenium.webdriver.remote.webdriver import WebDriver

from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
from parimana.base.race import Race
from parimana.netkeiba.browse import browse_odds_pages
from parimana.netkeiba.extract import extract_odds

# ratio_data = {
#     # https://jra.jp/company/about/financial/pdf/houkoku03.pdf p.26 別表9
#     BettingType.WIN: 6.9,
#     BettingType.QUINELLA: 13.3,
#     BettingType.EXACTA: 5.7,
#     BettingType.TRIO: 21.7,
#     BettingType.TRIFECTA: 29.0,
# }

ratio_data_derby = {
    # https://jra-van.jp/fun/baken/index3.html
    BettingType.WIN: 6.3,
    BettingType.QUINELLA: 16.3,
    BettingType.EXACTA: 6.3,
    BettingType.TRIO: 19.5,
    BettingType.TRIFECTA: 37.1,
}

vote_total = 100_000_000


@dataclass(frozen=True)
class NetKeibaRace(Race):
    netkeiba_race_id: str
    driver: WebDriver

    @cached_property
    def contestants(self) -> Contestants:
        names = [eye.text for eye in self.odds.keys() if eye.type == BettingType.WIN]
        return Contestants.from_names(names)

    @property
    def vote_ratio(self) -> Mapping[BettingType, float]:
        return ratio_data_derby

    @property
    def vote_tally_total(self) -> float:
        return 100_000_000

    @property
    def race_id(self) -> str:
        return self.netkeiba_race_id

    def collect_odds(self) -> Mapping[Eye, float]:
        return {
            eye: odds
            for content, btype in browse_odds_pages(self.driver, self.race_id)
            for eye, odds in extract_odds(content, btype).items()
        }
