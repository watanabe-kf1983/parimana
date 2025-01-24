from dataclasses import dataclass
import datetime

from parimana.domain.race import (
    OddsTimeStamp,
    RaceOddsPool,
    OddsSource,
)
from parimana.external.kdreams.base import KeirinRace, category_keirin
import parimana.external.kdreams.odds.browse as browser
from parimana.external.kdreams.odds.extract import (
    extract_odds,
    extract_timestamp,
    extract_ratio,
)
from parimana.external.kdreams.schedule.extract import extract_closing_time


@dataclass
class KeirinOddsSource(OddsSource):
    race: KeirinRace

    def scrape_odds_pool(self) -> RaceOddsPool:
        return _scrape_odds_pool(self.race)

    def scrape_timestamp(self) -> OddsTimeStamp:
        return _scrape_timestamp(self.race)

    def get_uri(self) -> str:
        return browser.get_uri(self.race)

    @classmethod
    def site_name(cls):
        return "kdreams.jp"


def _scrape_timestamp(race: KeirinRace) -> OddsTimeStamp:
    page = browser.browse_race(race)
    timestamp = extract_timestamp(page).replace(tzinfo=category_keirin.timezone)
    closing_time = extract_closing_time(page)
    closing_datetime = datetime.datetime.combine(
        race.meeting_day.date, closing_time, category_keirin.timezone
    )
    if timestamp > closing_datetime:
        return OddsTimeStamp.confirmed()
    else:
        return OddsTimeStamp(timestamp)


def _scrape_odds_pool(race: KeirinRace) -> RaceOddsPool:
    page = browser.browse_race(race)
    return RaceOddsPool(
        race=race,
        odds=extract_odds(page),
        timestamp=_scrape_timestamp(race),
        vote_ratio=extract_ratio(page),
    )
