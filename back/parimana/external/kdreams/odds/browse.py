from datetime import datetime

from parimana.external.kdreams import browser
from parimana.external.kdreams.base import KeirinRace


def browse_race(race: KeirinRace) -> str:
    return browser.get(get_uri(race), f"{datetime.now():%Y%m%d%H%M}")


def get_uri(race: KeirinRace) -> str:
    return (
        f"https://keirin.kdreams.jp/{race.meeting_day.meeting.studium.name_en}/"
        f"racedetail/{race.code}/"
    )
