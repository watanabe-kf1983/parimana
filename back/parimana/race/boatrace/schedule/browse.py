from datetime import datetime

import parimana.race.boatrace.browser as browser


def browse_day_index(date: datetime.date) -> str:
    return browser.get(_day_index_page_uri(date), f"{datetime.now():%Y%m%d%H%M}")


def browse_schedule(date: datetime.date, jo_code: str) -> str:
    return browser.get(
        _race_schedule_page_uri(date, jo_code), f"{datetime.now():%Y%m%d%H%M}"
    )


def _day_index_page_uri(date: datetime.date) -> str:
    return f"https://www.boatrace.jp/owpc/pc/race/index?hd={date:%Y%m%d}"


def _race_schedule_page_uri(date: datetime.date, jo_code: str) -> str:
    return (
        "https://www.boatrace.jp/owpc/pc/race/raceindex?"
        f"jcd={jo_code}&hd={date:%Y%m%d}"
    )
