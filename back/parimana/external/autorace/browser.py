from datetime import timedelta
from typing import Callable, Sequence

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from parimana.io.message import mprint
from parimana.devices.chrome import headless_chrome
from parimana.external.scraping_utils.modest import ModestFunction
from parimana.external.autorace.base import AutoRace


modestly = ModestFunction(interval=timedelta(seconds=1.5))

get_driver: Callable[[], WebDriver] = headless_chrome

modestly = ModestFunction(interval=timedelta(seconds=1.5))


class NoContentError(Exception):
    pass


@modestly
def get(uri: str, wait_selectors: Sequence[str]):
    driver = get_driver()
    mprint(f"opening {uri} ...")
    driver.get(uri)

    selectors = [
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        for selector in wait_selectors
    ]
    try:
        WebDriverWait(driver, 2).until(EC.all_of(*selectors))
        return driver.page_source

    except TimeoutException:
        raise NoContentError()


def browse_race_info_page(race: AutoRace) -> str:
    wait_selectors = [
        "#race-result-race-period-time > div:nth-child(2)",
    ]
    return get(_race_page_uri(race), wait_selectors)


def browse_race_odds_page(race: AutoRace) -> str:
    wait_selectors = [
        "#live-odds-pop-container table.liveTable.liveTable-ninki",
    ]
    return get(_race_page_uri(race), wait_selectors)


def _race_page_uri(race: AutoRace) -> str:
    return (
        f"https://autorace.jp/race_info/Odds/"
        f"{race.studium.name_en}/{race.date:%Y-%m-%d}_{race.race_no}/rt3"
    )
