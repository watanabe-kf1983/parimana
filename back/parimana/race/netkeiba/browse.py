from typing import Iterator, Tuple

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.expected_conditions import all_of
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from parimana.base.eye import BettingType
from parimana.driver.chrome import headless_chrome
from parimana.race.netkeiba.base import btype_to_code, supported_types


def browse_odds_pages(nk_race_id: str) -> Iterator[Tuple[str, BettingType]]:
    driver: WebDriver = headless_chrome()

    for btype in supported_types:
        for page_content in _browse_odds_by_btype(driver, nk_race_id, btype):
            yield (page_content, btype)


def _browse_odds_by_btype(
    driver: WebDriver, nk_race_id: str, btype: BettingType
) -> Iterator[str]:
    uri = _odds_page_uri(nk_race_id, btype)
    print(f"opening {uri} ...", end=" ", flush=True)
    driver.get(uri)
    print("done.", flush=True)

    if btype.size < 3:
        yield driver.page_source

    else:
        dropdown = driver.find_element(By.CSS_SELECTOR, "#list_select_horse")
        options = dropdown.find_elements(By.CSS_SELECTOR, "option")
        axis_numbers = {elem.get_attribute("value") for elem in options}

        for axis in axis_numbers:
            print(f" downloading axis {axis} odds...", end=" ", flush=True)
            dropdown = driver.find_element(By.CSS_SELECTOR, "#list_select_horse")
            Select(dropdown).select_by_value(axis)
            WebDriverWait(driver, timeout=10).until(_axis_is_loaded(axis))
            print("done.", flush=True)
            yield driver.page_source


def _axis_is_loaded(axis: str):
    return all_of(
        text_to_be_present_matched_on_element(
            (By.CSS_SELECTOR, "div.Axis_Horse span.Num"), axis
        ),
        no_text_in_page_source("---.-"),
    )


def no_text_in_page_source(text_):
    def _predicate(driver):
        return not (text_ in driver.page_source)

    return _predicate


def text_to_be_present_matched_on_element(locator, text_):
    def _predicate(driver):
        try:
            element_text = driver.find_element(*locator).text
            return text_ == element_text  # check complete match
        except StaleElementReferenceException:
            return False

    return _predicate


def _odds_page_uri(nk_race_id: str, btype: BettingType) -> str:
    return (
        "https://race.netkeiba.com/odds/index.html"
        f"?race_id={nk_race_id}&type=b{btype_to_code(btype)}"
    )
