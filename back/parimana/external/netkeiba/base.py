from dataclasses import dataclass
import datetime
import re
from typing import Optional, Sequence, Type
from zoneinfo import ZoneInfo

from parimana.domain.race import Race, OddsSource
from parimana.domain.schedule import Category, ScheduleSource


_keiba_timezone = ZoneInfo("Asia/Tokyo")


class _CategoryJra(Category):
    @property
    def id(self) -> str:
        return "hj"

    @property
    def name(self) -> str:
        return "中央競馬"

    @property
    def schedule_source(self) -> ScheduleSource:
        from parimana.external.netkeiba.schedule.scrape import jra_schedule_source

        return jra_schedule_source

    def has_race(self, race_id: str) -> bool:
        return bool(JraRace.from_id(race_id))

    @property
    def timezone(self) -> ZoneInfo:
        return _keiba_timezone

    @property
    def poll_start_time(self) -> datetime.time:
        return datetime.time(hour=8, minute=30)


class _CategoryNar(Category):
    @property
    def id(self) -> str:
        return "hn"

    @property
    def name(self) -> str:
        return "地方競馬"

    @property
    def schedule_source(self) -> ScheduleSource:
        raise NotImplementedError()
        # from parimana.external.netkeiba.schedule.scrape import jra_schedule_source
        # return jra_schedule_source

    def has_race(self, race_id: str) -> bool:
        return bool(NarRace.from_id(race_id))

    @property
    def timezone(self) -> ZoneInfo:
        return _keiba_timezone

    @property
    def poll_start_time(self) -> datetime.time:
        return datetime.time(hour=8, minute=30)


category_jra = _CategoryJra()
category_nar = _CategoryNar()


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
        from parimana.external.netkeiba.odds.scrape import NkJraRaceSource

        return NkJraRaceSource

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
        return f"hr{self.netkeiba_race_id}"

    @property
    def odds_source(self) -> OddsSource:
        return self.odds_source_type()(self)

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        raise NotImplementedError()
        # from parimana.external.netkeiba.odds.scrape import NkJraSource

        # return NkJraSource

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
