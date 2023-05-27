import time
from typing import Mapping

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select

from parimana.base.eye import BettingType, Eye


type_dict: Mapping[BettingType, str] = {
    BettingType.WIN: "1",
    BettingType.EXACTA: "6",
    BettingType.QUINELLA: "4",
    BettingType.TRIO: "7",
    BettingType.TRIFECTA: "8",
}
type_dict_inv: Mapping[str, BettingType] = {v: k for k, v in type_dict.items()}

# def type_id(bt: BettingType) -> str:


def get_webdriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(chrome_options=options)


def scrape(race_id: str = "202305021211"):
    driver = get_webdriver()
    return {
        eye: odds
        for btype in BettingType
        for eye, odds in scrape_by_btype(driver, race_id=race_id, btype=btype).items()
    }


def scrape_by_btype(
    driver: webdriver.Chrome, race_id: str, btype: BettingType
) -> Mapping[Eye, float]:
    print(f"scraping {race_id} {btype.name} odds...")
    uri = netkeiba_page_uri(race_id, btype)
    driver.get(uri)
    print(f"page {uri} got")

    odds = dict(extract_odds(driver.page_source, btype))
    if btype.size >= 3:
        dropdown = driver.find_element(value="list_select_horse")
        select_size = len(Select(dropdown).options)

        for i in range(select_size):
            dropdown = driver.find_element(value="list_select_horse")
            Select(dropdown).select_by_index(i)
            print(".", end="", flush=True)
            time.sleep(1)
            odds |= extract_odds(driver.page_source, btype)

    return odds


def netkeiba_page_uri(race_id: str, btype: BettingType) -> str:
    return (
        "https://race.netkeiba.com/odds/index.html"
        f"?race_id={race_id}&type=b{type_dict[btype]}"
    )


def extract_odds(html: str, btype: BettingType) -> Mapping[Eye, float]:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    elements = soup.select(f"table td.Odds span[id^='odds-{type_dict[btype]}']")
    return {elem_id_to_eye(e["id"]): float(e.get_text()) for e in elements}


def elem_id_to_eye(id: str):
    _, btype_code, number = id.replace("_", "-").split("-")
    betting_type = type_dict_inv[btype_code]
    names = [number[i : i + 2] for i in range(0, len(number), 2)]
    return Eye.from_names(names, betting_type)
