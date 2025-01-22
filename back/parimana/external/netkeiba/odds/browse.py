from dataclasses import dataclass
from functools import cached_property
from typing import Iterator, Tuple

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.expected_conditions import all_of
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from parimana.io.message import mprint
from parimana.domain.base import BettingType
from parimana.external.netkeiba.base import NetKeibaRace
from parimana.external.netkeiba.odds.btype import btype_to_code, supported_types
from parimana.external.netkeiba.browser import get_driver, modestly


@dataclass
class NetKeibaOddsBrowser:
    host_name: str
    race: NetKeibaRace

    @cached_property
    def _dwrapper(self):
        return DriverWrapper(get_driver())

    @cached_property
    def _uri_provider(self):
        return OddsUriProvider(self.host_name, self.race)

    def get_source_uri(self) -> str:
        return self._uri_provider.odds_uri_base

    def browse_for_odds_timestamp(self) -> str:
        dw = self._dwrapper
        dw.refresh()
        dw.go_to(self._uri_provider.odds_uri(BettingType.WIN))
        return dw.page_source()

    def browse_odds_pages(self) -> Iterator[Tuple[str, BettingType]]:

        dw = self._dwrapper
        for btype in supported_types:

            dw.go_to(self._uri_provider.odds_uri(btype))
            if btype.size < 3:
                yield dw.page_source(), btype

            else:
                for source in _browse_all_axis(dw.driver):
                    yield source, btype


@dataclass
class OddsUriProvider:
    host_name: str
    race: NetKeibaRace

    @cached_property
    def odds_uri_base(self) -> str:
        return (
            f"https://{self.host_name}/odds/index.html"
            f"?race_id={self.race.netkeiba_race_id}"
        )

    def odds_uri(self, btype: BettingType) -> str:
        return f"{self.odds_uri_base}&type=b{btype_to_code(btype)}"


@dataclass
class DriverWrapper:
    driver: WebDriver

    def go_to(self, uri):
        if uri != self.driver.current_url:
            self._get(uri)

    def refresh(self):
        self.driver.delete_all_cookies()
        self.driver.refresh()

    def page_source(self):
        return self.driver.page_source

    @modestly
    def _get(self, uri):
        mprint(f"opening {uri} ...")
        self.driver.get(uri)


def _browse_all_axis(driver: WebDriver) -> Iterator[str]:

    dropdown = driver.find_element(By.CSS_SELECTOR, "#list_select_horse")
    options = dropdown.find_elements(By.CSS_SELECTOR, "option")
    axis_numbers = {elem.get_attribute("value") for elem in options}

    for axis in axis_numbers:
        if axis:
            _download_axis(driver, axis, dropdown)
            yield driver.page_source


@modestly
def _download_axis(driver: WebDriver, axis, dropdown):
    mprint(f" downloading axis {axis} odds...")
    dropdown = driver.find_element(By.CSS_SELECTOR, "#list_select_horse")
    Select(dropdown).select_by_value(axis)
    WebDriverWait(driver, timeout=10).until(_axis_is_loaded(axis))


def _axis_is_loaded(axis: str):
    return all_of(
        _text_to_be_present_matched_on_element(
            (By.CSS_SELECTOR, "div.Axis_Horse span.Num"), axis
        ),
        _no_text_in_page_source("---.-"),
    )


def _no_text_in_page_source(text_):
    def _predicate(driver: WebDriver):
        return not (text_ in driver.page_source)

    return _predicate


def _text_to_be_present_matched_on_element(locator, text_):
    def _predicate(driver: WebDriver):
        try:
            element_text = driver.find_element(*locator).text
            return text_ == element_text  # check complete match
        except StaleElementReferenceException:
            return False

    return _predicate
