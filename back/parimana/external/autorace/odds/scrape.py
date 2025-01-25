from dataclasses import dataclass
import datetime

from parimana.domain.race import (
    OddsTimeStamp,
    RaceOddsPool,
    OddsSource,
)
from parimana.external.autorace.base import AutoRace, category_moto
import parimana.external.autorace.browser as browser
from parimana.external.autorace.odds.extract import (
    extract_odds,
    extract_timestamp_text,
    extract_ratio,
)


@dataclass
class MotoOddsSource(OddsSource):
    race: AutoRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        return _scrape_odds_pool(self.race)

    def scrape_timestamp(self) -> OddsTimeStamp:
        return _scrape_timestamp(self.race)

    def get_uri(self) -> str:
        return browser.race_page_uri(self.race)

    @classmethod
    def site_name(cls):
        return "autorace.jp"


def _scrape_timestamp(race: AutoRace) -> OddsTimeStamp:
    page = browser.browse_race_odds_page(race)
    return _extract_odds_timestamp(page, race.date)


def _scrape_odds_pool(race: AutoRace) -> RaceOddsPool:
    page = browser.browse_race_odds_page(race)
    return RaceOddsPool(
        race=race,
        odds=extract_odds(page),
        timestamp=_extract_odds_timestamp(page, race.date),
        vote_ratio=extract_ratio(page),
    )


def _extract_odds_timestamp(page, date: datetime.date) -> OddsTimeStamp:
    timestamp_text = extract_timestamp_text(page)
    if timestamp_text == "オッズ確定":
        return OddsTimeStamp.confirmed()
    else:
        odds_time = datetime.datetime.strptime(timestamp_text, "オッズ更新 %H:%M")
        odds_datetime = datetime.datetime.combine(
            date, odds_time, category_moto.timezone
        )
        return OddsTimeStamp(odds_datetime)
