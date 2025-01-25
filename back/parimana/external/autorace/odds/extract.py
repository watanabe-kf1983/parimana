import re
from typing import Mapping, Optional, Sequence

import numpy as np
from bs4 import BeautifulSoup

from parimana.domain.base.eye import BettingType, Eye
from parimana.domain.base.odds import Odds

container_selector_by_btype = {
    BettingType.WIN: "#live-odds-tns-container",
    BettingType.PLACE: "#live-odds-fns-container",
    BettingType.SHOW: "#live-odds-fns-container",
    BettingType.EXACTA: "#live-odds-rt2-container",
    BettingType.QUINELLA: "#live-odds-rf2-container",
    BettingType.WIDE: "#live-odds-wid-container",
    BettingType.TRIFECTA: "#live-odds-rt3-container",
    BettingType.TRIO: "#live-odds-rf3-container",
}

VOTE_COUNT_PATTERN: re.Pattern = re.compile(r"発売票数:(?P<count>[0-9]+) ")


def _btypes(soup: BeautifulSoup) -> Sequence[BettingType]:
    type_list = [
        type
        for type in container_selector_by_btype.keys()
        if type not in [BettingType.PLACE, BettingType.SHOW]
    ]

    no8_exists = bool(
        len(soup.select("#live-odds-rt3-container table.liveTable-Info .raceNum--08"))
    )
    if not no8_exists:
        # 7車立て以下の場合は複勝は2着まで
        # https://isesaki-auto.jp/beginner/post/
        type_list.append(BettingType.PLACE)
    else:
        type_list.append(BettingType.SHOW)

    return type_list


def extract_odds(html: str) -> Mapping[Eye, Odds]:
    soup = _parse(html)
    return {
        eye: odds
        for btype in _btypes(soup)
        for eye, odds in _extract_odds_by_btype(soup, btype).items()
    }


def extract_ratio(html: str) -> Mapping[BettingType, float]:
    soup = _parse(html)
    return {btype: _extract_vote_count(soup, btype) for btype in _btypes(soup)}


def extract_timestamp_text(html: str) -> str:
    soup = _parse(html)
    return soup.select_one("#updated_odds_time_display").get_text()


def _extract_odds_by_btype(
    soup: BeautifulSoup, btype: BettingType
) -> Mapping[Eye, Odds]:
    container = soup.select_one(container_selector_by_btype[btype])
    elements = container.select(
        "table.liveTable td.text-right:not("
        ".raceNum--01,.raceNum--02,.raceNum--03,.raceNum--04,"
        ".raceNum--05,.raceNum--06,.raceNum--07,.raceNum--08"
        ")"
    )
    extracted_text = [elem.get_text(strip=True).replace("～", "-") for elem in elements]
    table_orderd_eyes = _eyes_table_order(btype)
    return {
        eye: Odds.from_text(odds_text)
        for eye, odds_text in zip(table_orderd_eyes, extracted_text)
        if eye and odds_text
    }


def _eyes_table_order(btype: BettingType) -> Sequence[Optional[Eye]]:
    names = [str(i) for i in range(1, 8 + 1)]

    if btype == BettingType.TRIFECTA:
        return _trifecta_eyes_table_order(names)
    elif btype == BettingType.TRIO:
        return _trio_eyes_table_order(names)
    elif btype == BettingType.EXACTA:
        return _exacta_eyes_table_order(names)
    elif btype == BettingType.WIDE or btype == BettingType.QUINELLA:
        return _combi_eyes_table_order(names, btype)
    else:  # win, show, place
        return Eye.all_eyes(names, btype)


def _trifecta_eyes_table_order(names: Sequence[str]) -> Sequence[Eye]:
    all_eyes = Eye.all_eyes(names, BettingType.TRIFECTA)
    size = len(names)
    size_half = size // 2
    slices = list(np.split(np.array(all_eyes), size))
    splitted = [
        b
        for i, a in enumerate(slices)
        for b in np.split(
            a.reshape(size - 1, -1),
            [size_half - 1 if i < size_half else size_half],
        )
    ]
    return [eye for block in splitted for eye in block.T.reshape(-1)]


def _trio_eyes_table_order(names: Sequence[str]) -> Sequence[Optional[Eye]]:
    def convert_to_trio(e: Eye):
        a, b, c = e.names
        if a < b < c:
            return Eye.from_names(list(e.names), BettingType.TRIO)
        else:
            return None

    return [convert_to_trio(e) for e in _trifecta_eyes_table_order(names)]


def _exacta_eyes_table_order(names: Sequence[str]) -> Sequence[Eye]:
    all_eyes = Eye.all_eyes(names, BettingType.EXACTA)
    splitted = list(np.split(np.array(all_eyes), 2))
    size = len(names)
    return [
        eye for block in splitted for eye in block.reshape(size // 2, -1).T.reshape(-1)
    ]


def _combi_eyes_table_order(
    names: Sequence[str], btype: BettingType
) -> Sequence[Optional[Eye]]:

    def convert_to_combi(e: Eye):
        a, b = e.names
        if a < b:
            return Eye.from_names(list(e.names), btype)
        else:
            return None

    return [convert_to_combi(e) for e in _exacta_eyes_table_order(names)]


def _extract_vote_count(soup: BeautifulSoup, btype: BettingType) -> int:
    vote_count_text = (
        soup.select_one(container_selector_by_btype[btype])
        .select_one("div.alert.alert-light p")
        .get_text()
        .replace(",", "")
    )
    if m := re.search(VOTE_COUNT_PATTERN, vote_count_text):
        return float(m.group("count"))
    else:
        raise ValueError("Failed parse vote count string: " + vote_count_text)


def _parse(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")


# 欠車の例 https://autorace.jp/race_info/Odds/kawaguchi/2017-11-11_11/rt3
