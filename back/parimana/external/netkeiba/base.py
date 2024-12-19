from dataclasses import dataclass
import re
from typing import Optional
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


category_keiba = _CategoryNetKeiba()


@dataclass
class NetKeibaRace(Race):
    netkeiba_race_id: str

    @property
    def race_id(self) -> str:
        return f"hr{self.netkeiba_race_id}"

    @property
    def odds_source(self) -> OddsSource:
        from parimana.external.netkeiba.odds.scrape import NetKeibaSource

        return NetKeibaSource(self)

    @classmethod
    def from_id(cls, race_id: str) -> Optional[Race]:
        if m := re.fullmatch(_RACE_ID_PATTERN, race_id):
            return NetKeibaRace(**m.groupdict())
        else:
            return None


_RACE_ID_PATTERN: re.Pattern = re.compile(r"hr(?P<netkeiba_race_id>[0-9]{12})")
