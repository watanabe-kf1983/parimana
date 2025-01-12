from datetime import timedelta
from typing import Callable

from selenium.webdriver.remote.webdriver import WebDriver

from parimana.io.message import mprint
from parimana.external.scraping_utils.modest import ModestFunction
from parimana.devices.chrome import headless_chrome


modestly = ModestFunction(interval=timedelta(seconds=1.5))

get_driver: Callable[[], WebDriver] = headless_chrome


@modestly
def get(uri: str):
    driver = get_driver()
    mprint(f"opening {uri} ...")
    driver.get(uri)
    return driver.page_source
