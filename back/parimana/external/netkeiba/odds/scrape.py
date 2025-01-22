from abc import abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Mapping, Tuple

from parimana.io.message import mprint
from parimana.domain.base import Eye, Odds
from parimana.domain.race import (
    OddsTimeStamp,
    OddsUpdatedException,
    RaceOddsPool,
    OddsSource,
)
from parimana.external.netkeiba.base import NetKeibaRace
from parimana.external.netkeiba.odds.data import ratio_data
from parimana.external.netkeiba.odds.extract import (
    JraOddsExtractor,
    NarOddsExtractor,
    NetKeibaOddsExtractor,
)
from parimana.external.netkeiba.odds.browse import NetKeibaOddsBrowser


@dataclass
class NetKeibaOddsSource(OddsSource):
    race: NetKeibaRace

    @cached_property
    def browser(self):
        return NetKeibaOddsBrowser(self.site_name(), self.race)

    @abstractmethod
    def extractor(self) -> NetKeibaOddsExtractor:
        pass

    def scrape_odds_pool(self) -> RaceOddsPool:
        return _scrape_odds_pool(self.browser, self.extractor())

    def scrape_timestamp(self) -> OddsTimeStamp:
        return _scrape_timestamp(self.browser, self.extractor())

    def get_uri(self) -> str:
        return self.browser.get_source_uri()


@dataclass
class JraOddsSource(NetKeibaOddsSource):

    def extractor(self) -> NetKeibaOddsExtractor:
        return JraOddsExtractor()

    @classmethod
    def site_name(cls):
        return "race.netkeiba.com"


@dataclass
class NarOddsSource(NetKeibaOddsSource):

    def extractor(self) -> NetKeibaOddsExtractor:
        return NarOddsExtractor()

    @classmethod
    def site_name(cls):
        return "nar.netkeiba.com"


def _scrape_odds_pool(
    browser: NetKeibaOddsBrowser, extractor: NetKeibaOddsExtractor
) -> RaceOddsPool:
    odds, timestamp = _collect_odds(browser, extractor)
    return RaceOddsPool(
        race=browser.race,
        odds=odds,
        timestamp=timestamp,
        vote_ratio=ratio_data,
    )


def _scrape_timestamp(
    browser: NetKeibaOddsBrowser, extractor: NetKeibaOddsExtractor
) -> OddsTimeStamp:
    html = browser.browse_for_odds_timestamp()
    return extractor.extract_timestamp(html)


def _collect_odds(
    browser: NetKeibaOddsBrowser, extractor: NetKeibaOddsExtractor
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:
    for attempt in ["1st", "2nd"]:
        try:
            return _attempt_collect_odds(browser, extractor)
        except OddsUpdatedException:
            pass

    raise ValueError("collect_odds Failed")


def _attempt_collect_odds(
    browser: NetKeibaOddsBrowser, extractor: NetKeibaOddsExtractor
) -> Tuple[Mapping[Eye, Odds], OddsTimeStamp]:

    odds: dict[Eye, Odds] = {}
    timestamp = _scrape_timestamp(browser, extractor)

    for content, btype in browser.browse_odds_pages():
        if extractor.extract_timestamp(content) != timestamp:
            mprint("Odds update detected")
            raise OddsUpdatedException()

        odds |= extractor.extract_odds(content, btype)

    return odds, timestamp
