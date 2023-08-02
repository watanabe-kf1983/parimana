from dataclasses import dataclass, field
from functools import cached_property
import re
from typing import ClassVar, Mapping, Optional

from selenium.webdriver.remote.webdriver import WebDriver

from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.base.race import Race
from parimana.driver.chrome import headless_chrome
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



@dataclass
class NetKeibaRace(Race):
    netkeiba_race_id: str
    driver: WebDriver = field(default_factory=headless_chrome)

    @cached_property
    def contestants(self) -> Contestants:
        names = [eye.text for eye in self.odds.keys() if eye.type == BettingType.WIN]
        return Contestants.from_names(names)

    @property
    def vote_ratio(self) -> Mapping[BettingType, float]:
        return ratio_data_derby

    @property
    def race_id(self) -> str:
        return f"netkeiba-{self.netkeiba_race_id}"

    def collect_odds(self) -> Mapping[Eye, Odds]:
        return {
            eye: odds
            for content, btype in browse_odds_pages(self.driver, self.netkeiba_race_id)
            for eye, odds in extract_odds(content, btype).items()
        }

    PATTERN: ClassVar[str] = re.compile(r"netkeiba-(?P<netkeiba_race_id>[0-9]{12})")

    @classmethod
    def from_race_id(cls, race_id: str) -> Optional["NetKeibaRace"]:
        if m := re.fullmatch(cls.PATTERN, race_id):
            return NetKeibaRace(**m.groupdict())
        else:
            return None
