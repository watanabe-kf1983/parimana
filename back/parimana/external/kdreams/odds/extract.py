import datetime
from typing import Collection, Mapping, Sequence

from bs4 import BeautifulSoup

from parimana.domain.base.eye import BettingType, Eye
from parimana.domain.base.odds import Odds

btype_div_id_suffix = {
    BettingType.WIDE: "wide",
    BettingType.QUINELLA: "2shahuku",
    BettingType.EXACTA: "2shatan",
    BettingType.TRIO: "3renhuku",
    BettingType.TRIFECTA: "3rentan",
}
supported_types: Collection[BettingType] = btype_div_id_suffix.keys()


def extract_odds(html: str) -> Mapping[Eye, Odds]:
    soup = parse(html)
    return {
        eye: odds
        for btype in supported_types
        for eye, odds in extract_odds_by_btype(soup, btype).items()
    }


def extract_ratio(html: str) -> Mapping[BettingType, float]:
    soup = parse(html)
    return {
        btype: float(
            soup.select_one(f"#JS_ODDSSTATUS_{btype_div_id_suffix[btype]}")
            .select_one("dl.number dd")
            .get_text()
            .replace(",", "")
        )
        for btype in supported_types
    }


def extract_timestamp(html: str) -> datetime.datetime:
    soup = parse(html)
    update_txt = (
        soup.select_one("#JS_ODDSSTATUS_3renhuku").select_one("p.time").get_text()
    )
    return datetime.datetime.strptime(update_txt, "%Y/%m/%d %H:%M現在")


def extract_odds_by_btype(
    soup: BeautifulSoup, btype: BettingType
) -> Mapping[Eye, Odds]:
    div = soup.select_one(f"#JS_ODDSCONTENTS_{btype_div_id_suffix[btype]}")
    elements = div.select("div.odds_table_wrapper table td:not(.rider,.empty)")
    extracted = [
        Odds.from_text(elem.get_text().replace("～", "-")) for elem in elements
    ]
    names = extract_names(soup)
    eyes = eyes_table_order(names, btype)
    return {eye: odds for eye, odds in zip(eyes, extracted) if odds}


def extract_names(soup: BeautifulSoup) -> Sequence[str]:
    return [e.get_text() for e in soup.select("#RENTAN dl.odds-order_nav a")]


def eyes_table_order(names: Sequence[str], btype: BettingType) -> Sequence[Eye]:
    all_eyes = Eye.all_eyes(names, btype)

    if btype == BettingType.TRIFECTA:  # exacta, trifecta
        return sorted(all_eyes, key=lambda e: e.names[0] + e.names[2] + e.names[1])
    elif btype == BettingType.EXACTA:
        return sorted(all_eyes, key=lambda e: e.names[1] + e.names[0])
    elif btype == BettingType.WIDE or btype == BettingType.QUINELLA:
        return sorted(all_eyes, key=lambda e: sorted(e.names)[1] + sorted(e.names)[0])
    else:  # trio
        return all_eyes


def parse(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
