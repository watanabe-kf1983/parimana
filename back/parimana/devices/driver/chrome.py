from typing import Optional
from selenium import webdriver

_headless_chrome: Optional[webdriver.Chrome] = None


def headless_chrome() -> webdriver.Chrome:
    global _headless_chrome
    if not _headless_chrome:
        _headless_chrome = create_headless_chrome()
    return _headless_chrome


def create_headless_chrome() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # ChromeDriverがログを吐きまくる対策
    # https://github.com/SeleniumHQ/selenium/issues/13095
    options.add_argument("--log-level=3")
    options.set_capability("browserVersion", "117")

    return webdriver.Chrome(options=options)
