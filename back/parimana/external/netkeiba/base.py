from dataclasses import dataclass
import datetime
import re
from typing import Optional, Type
from zoneinfo import ZoneInfo

from parimana.domain.race import Race, OddsSource
from parimana.domain.schedule import Category, ScheduleSource


_keiba_timezone = ZoneInfo("Asia/Tokyo")


class _CategoryNetKeiba(Category):
    @property
    def id(self) -> str:
        return "hr"

    @property
    def name(self) -> str:
        return "競馬"

    @property
    def schedule_source(self) -> ScheduleSource:
        from parimana.external.netkeiba.schedule.scrape import schedule_source

        return schedule_source

    @property
    def timezone(self) -> ZoneInfo:
        return _keiba_timezone

    @property
    def poll_start_time(self) -> datetime.time:
        return datetime.time(hour=8, minute=30)


category_keiba = _CategoryNetKeiba()


@dataclass
class NetKeibaRace(Race):
    netkeiba_race_id: str

    @property
    def race_id(self) -> str:
        return f"hr{self.netkeiba_race_id}"

    @property
    def odds_source(self) -> OddsSource:
        return self.odds_source_type()(self)

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        from parimana.external.netkeiba.odds.scrape import NetKeibaSource

        return NetKeibaSource

    @classmethod
    def from_id(cls, race_id: str) -> Optional[Race]:
        if m := re.fullmatch(_RACE_ID_PATTERN, race_id):
            return cls(**m.groupdict())
        else:
            return None

    @classmethod
    def from_uri(cls, uri: str) -> Optional[Race]:
        if not any(
            phrase in uri
            for phrase in [
                "race.sp.netkeiba.com",
                "race.netkeiba.com",
            ]
        ):
            return None

        try:
            if m := re.search(_URI_RACE_ID_PATTERN, uri):
                return cls(**m.groupdict())
            else:
                return None

        except Exception:
            return None


_RACE_ID_PATTERN: re.Pattern = re.compile(r"hr(?P<netkeiba_race_id>[0-9]{12})")
_URI_RACE_ID_PATTERN: re.Pattern = re.compile(
    r"race_id=(?P<netkeiba_race_id>[0-9]{12})"
)
