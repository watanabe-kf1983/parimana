from datetime import timedelta

from selenium.webdriver.remote.webdriver import WebDriver

from parimana.infra.message import mprint
from parimana.infra.browser.modest import ModestFunction
from parimana.devices.driver.chrome import headless_chrome


modestly = ModestFunction(interval=timedelta(seconds=1.5))

driver: WebDriver = headless_chrome()


@modestly
def get(uri: str):
    mprint(f"opening {uri} ...")
    driver.get(uri)
    return driver.page_source
