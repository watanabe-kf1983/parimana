from typing import Mapping
from selenium.webdriver.remote.webdriver import WebDriver
from parimana.base.eye import Eye

from parimana.scrape.netkeiba.browse import browse_odds_pages
from parimana.scrape.netkeiba.extract import extract_odds


def collect_odds(driver: WebDriver, race_id: str) -> Mapping[Eye, float]:
    return {
        eye: odds
        for content, btype in browse_odds_pages(driver, race_id)
        for eye, odds in extract_odds(content, btype).items()
    }
