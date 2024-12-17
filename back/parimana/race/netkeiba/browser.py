from datetime import timedelta

from selenium.webdriver.remote.webdriver import WebDriver

from parimana.message import mprint
from parimana.driver.chrome import headless_chrome
from parimana.driver.modest import ModestFunction


modestly = ModestFunction(interval=timedelta(seconds=1.5))

driver: WebDriver = headless_chrome()


@modestly
def get(uri: str):
    mprint(f"opening {uri} ...")
    driver.get(uri)
    return driver.page_source
