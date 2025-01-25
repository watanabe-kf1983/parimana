from dataclasses import dataclass
import datetime
import re
from typing import Optional, Sequence, Type
from zoneinfo import ZoneInfo

from parimana.domain.race import Race, OddsSource
from parimana.domain.schedule import Category, ScheduleSource


@dataclass
class NetKeibaRace(Race):
    netkeiba_race_id: str


@dataclass
class JraRace(NetKeibaRace):

    @property
    def race_id(self) -> str:
        return f"hj{self.netkeiba_race_id}"

    @property
    def odds_source(self) -> OddsSource:
        return self.odds_source_type()(self)

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        from parimana.external.netkeiba.odds.scrape import JraOddsSource

        return JraOddsSource

    @classmethod
    def from_id(cls, race_id: str) -> Optional["JraRace"]:
        if m := re.fullmatch(r"hj(?P<netkeiba_race_id>[0-9]{12})", race_id):
            return cls(**m.groupdict())
        else:
            return None

    @classmethod
    def from_uri(cls, uri: str) -> Optional["JraRace"]:
        if not contains_any_phrase(
            uri,
            phrases=[
                "race.sp.netkeiba.com",
                "race.netkeiba.com",
            ],
        ):
            return None

        if netkeiba_race_id := extract_netkeiba_id_from_uri(uri):
            return cls(netkeiba_race_id=netkeiba_race_id)


@dataclass
class NarRace(NetKeibaRace):

    @property
    def race_id(self) -> str:
        return f"hn{self.netkeiba_race_id}"

    @property
    def odds_source(self) -> OddsSource:
        return self.odds_source_type()(self)

    def kaisai_id(self) -> str:
        return self.netkeiba_race_id[:-2]

    def date(self) -> datetime.date:
        yyyymmdd = self.netkeiba_race_id[0:4] + self.netkeiba_race_id[6:10]
        return datetime.datetime.strptime(yyyymmdd, "%Y%m%d").date()

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        from parimana.external.netkeiba.odds.scrape import NarOddsSource

        return NarOddsSource

    @classmethod
    def from_id(cls, race_id: str) -> Optional["NarRace"]:
        if m := re.fullmatch(r"hn(?P<netkeiba_race_id>[0-9]{12})", race_id):
            return cls(**m.groupdict())
        else:
            return None

    @classmethod
    def from_uri(cls, uri: str) -> Optional["NarRace"]:
        if not contains_any_phrase(
            uri,
            phrases=[
                "nar.sp.netkeiba.com",
                "nar.netkeiba.com",
            ],
        ):
            return None

        if netkeiba_race_id := extract_netkeiba_id_from_uri(uri):
            return cls(netkeiba_race_id=netkeiba_race_id)


_URI_RACE_ID_PATTERN: re.Pattern = re.compile(
    r"race_id=(?P<netkeiba_race_id>[0-9]{12})"
)


def contains_any_phrase(text: str, phrases: Sequence[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def extract_netkeiba_id_from_uri(uri: str) -> Optional[str]:
    if m := re.search(_URI_RACE_ID_PATTERN, uri):
        return m.groupdict().get("netkeiba_race_id")


class _CategoryJra(Category):

    def __init__(self):
        super().__init__(
            id="hj",
            name="中央競馬",
            race_type=JraRace,
            timezone=_keiba_timezone,
            poll_start_time=datetime.time(hour=8, minute=0),
        )

    @property
    def schedule_source(self) -> ScheduleSource:
        from parimana.external.netkeiba.schedule.scrape import JraScheduleSource

        return JraScheduleSource()


class _CategoryNar(Category):

    def __init__(self):
        super().__init__(
            id="hn",
            name="地方競馬",
            race_type=NarRace,
            timezone=_keiba_timezone,
            poll_start_time=datetime.time(hour=10, minute=10),
        )

    @property
    def schedule_source(self) -> ScheduleSource:
        from parimana.external.netkeiba.schedule.scrape import NarScheduleSource

        return NarScheduleSource()


_keiba_timezone = ZoneInfo("Asia/Tokyo")


category_jra = _CategoryJra()
category_nar = _CategoryNar()
