from dataclasses import dataclass
import datetime
import re
from typing import Optional, Sequence, Type
from zoneinfo import ZoneInfo

from parimana.domain.race import Race, OddsSource
from parimana.domain.schedule import Category, ScheduleSource


@dataclass
class KeirinRace(Race):
    kdreams_race_id: str

    @property
    def race_id(self) -> str:
        return f"kr{self.kdreams_race_id}"

    @property
    def odds_source(self) -> OddsSource:
        return self.odds_source_type()(self)

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        raise NotImplementedError()
        # from parimana.external.netkeiba.odds.scrape import JraOddsSource

        # return JraOddsSource

    @classmethod
    def from_id(cls, race_id: str) -> Optional["KeirinRace"]:
        if m := re.fullmatch(r"kr(?P<kdreams_race_id>[0-9]{16})", race_id):
            return cls(**m.groupdict())
        else:
            return None

    @classmethod
    def from_uri(cls, uri: str) -> Optional["KeirinRace"]:
        if not contains_any_phrase(
            uri,
            phrases=[
                "keirin.kdreams.jp",
            ],
        ):
            return None

        if kdreams_race_id := extract_kdreams_id_from_uri(uri):
            return cls(kdreams_race_id=kdreams_race_id)


_URI_RACE_ID_PATTERN: re.Pattern = re.compile(
    r"racedetail/(?P<kdreams_race_id>[0-9]{16})/"
)


def contains_any_phrase(text: str, phrases: Sequence[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def extract_kdreams_id_from_uri(uri: str) -> Optional[str]:
    if m := re.search(_URI_RACE_ID_PATTERN, uri):
        return m.groupdict().get("netkeiba_race_id")


class _CategoryKeirin(Category):

    def __init__(self):
        super().__init__(
            id="kr",
            name="競輪",
            race_type=KeirinRace,
            timezone=_keirin_timezone,
            poll_start_time=datetime.time(hour=7, minute=30),
        )

    @property
    def schedule_source(self) -> ScheduleSource:
        raise NotImplementedError()
        # from parimana.external.netkeiba.schedule.scrape import JraScheduleSource

        # return JraScheduleSource()


_keirin_timezone = ZoneInfo("Asia/Tokyo")


category_keirin = _CategoryKeirin()
