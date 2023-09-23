from typing import Iterator, Tuple

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.expected_conditions import all_of
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from parimana.base import BettingType
from parimana.driver.chrome import headless_chrome
from parimana.race.netkeiba.btype import btype_to_code, supported_types
from parimana.race.netkeiba.race import NetKeibaRace


def browse_for_odds_timestamp(race: NetKeibaRace) -> str:
    driver: WebDriver = headless_chrome()
    get_page(driver, race, BettingType.WIN)
    update_odds(driver)
    return driver.page_source


def browse_odds_pages(race: NetKeibaRace) -> Iterator[Tuple[str, BettingType]]:
    driver: WebDriver = headless_chrome()

    for btype in supported_types:
        pages = _browse_odds_by_btype(driver, race, btype)

        for page_content in pages:
            yield (page_content, btype)


def _browse_odds_by_btype(
    driver: WebDriver, race: NetKeibaRace, btype: BettingType
) -> Iterator[str]:
    get_page(driver, race, btype)

    if btype.size < 3:
        yield driver.page_source

    else:
        dropdown = driver.find_element(By.CSS_SELECTOR, "#list_select_horse")
        options = dropdown.find_elements(By.CSS_SELECTOR, "option")
        axis_numbers = {elem.get_attribute("value") for elem in options}

        for axis in axis_numbers:
            if axis:
                print(f" downloading axis {axis} odds...", end=" ", flush=True)
                dropdown = driver.find_element(By.CSS_SELECTOR, "#list_select_horse")
                Select(dropdown).select_by_value(axis)
                WebDriverWait(driver, timeout=10).until(_axis_is_loaded(axis))
                print("done.", flush=True)
                yield driver.page_source


def update_odds(driver: WebDriver):
    driver.delete_all_cookies()
    driver.refresh()
    update_button = driver.find_element(By.CSS_SELECTOR, "#act-manual_update")
    if update_button.is_displayed():
        limit = get_odds_update_limit(driver)
        update_button.click()
        WebDriverWait(driver, timeout=10).until(odds_limit_updated(limit))


def get_odds_update_limit(driver: WebDriver):
    return driver.find_element(By.CSS_SELECTOR, "#OddsUpLimitCount").text


def odds_limit_updated(update_limit):
    def _predicate(driver: WebDriver):
        return update_limit != get_odds_update_limit(driver)

    return _predicate


def _axis_is_loaded(axis: str):
    return all_of(
        text_to_be_present_matched_on_element(
            (By.CSS_SELECTOR, "div.Axis_Horse span.Num"), axis
        ),
        no_text_in_page_source("---.-"),
    )


def no_text_in_page_source(text_):
    def _predicate(driver: WebDriver):
        return not (text_ in driver.page_source)

    return _predicate


def text_to_be_present_matched_on_element(locator, text_):
    def _predicate(driver: WebDriver):
        try:
            element_text = driver.find_element(*locator).text
            return text_ == element_text  # check complete match
        except StaleElementReferenceException:
            return False

    return _predicate


def get_page(driver: WebDriver, race: NetKeibaRace, btype: BettingType):
    uri = _odds_page_uri(race, btype)
    if uri != driver.current_url:
        print(f"opening {uri} ...", end=" ", flush=True)
        driver.get(uri)
        print("done.", flush=True)


def _odds_page_uri(race: NetKeibaRace, btype: BettingType) -> str:
    return (
        "https://race.netkeiba.com/odds/index.html"
        f"?race_id={race.netkeiba_race_id}&type=b{btype_to_code(btype)}"
    )
