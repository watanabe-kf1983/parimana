import logging
from typing import Optional

from selenium import webdriver


_headless_chrome: Optional[webdriver.Chrome] = None


def headless_chrome() -> webdriver.Chrome:
    global _headless_chrome
    if not _headless_chrome:
        logger = logging.getLogger("selenium")
        lev = logger.getEffectiveLevel()
        logger.setLevel(logging.DEBUG)

        _headless_chrome = create_headless_chrome()

        logger.setLevel(lev)

    return _headless_chrome


def create_headless_chrome() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(options=options)
