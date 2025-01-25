from dataclasses import dataclass
import datetime
import re
from typing import Mapping, Optional, Sequence, Type
from zoneinfo import ZoneInfo

from parimana.domain.race import Race, OddsSource
from parimana.domain.schedule import Category, ScheduleSource, Course


@dataclass
class MotoStudium:
    code: str
    name: str
    name_en: str

    def to_course(self):
        return Course(id=f"MT{self.code}", name=self.name, category=category_moto)

    @classmethod
    def from_code(cls, code: str):
        return _code_studium_map.get(code)

    @classmethod
    def from_name_en(cls, name_en: str):
        return _name_en_studium_map.get(name_en)


all_studiums: Sequence[MotoStudium] = [
    MotoStudium(code, name, name_en)
    for name, name_en, code in (
        studium_text.split("/")
        for studium_text in (
            # https://autorace.jp/pdf/tel_guide.pdf p.14
            # https://ctc.gr.jp/link/
            "川口/kawaguchi/02 伊勢崎/isesaki/03 浜松/hamamatsu/04 飯塚/iizuka/05 山陽/sanyou/06"
        ).split()
    )
]
_code_studium_map: Mapping[str, MotoStudium] = {std.code: std for std in all_studiums}
_name_en_studium_map: Mapping[str, MotoStudium] = {
    std.name_en: std for std in all_studiums
}


@dataclass
class AutoRace(Race):
    date: datetime.date
    studium: MotoStudium
    race_no: int

    @property
    def name(self) -> str:
        return f"{self.race_no}R"

    @property
    def race_id(self) -> str:
        return f"MT{self.date:%Y%m%d}{self.studium.code}{self.race_no:02}"

    @classmethod
    def from_id(cls, race_id: str) -> Optional["AutoRace"]:
        if m := re.fullmatch(_RACE_ID_PATTERN, race_id):
            return cls(
                date=datetime.datetime.strptime(m.group("date"), "%Y%m%d").date(),
                studium=MotoStudium.from_code(m.group("studium_code")),
                race_no=int(m.group("race_no")),
            )
        else:
            return None

    @classmethod
    def from_uri(cls, uri: str) -> Optional["AutoRace"]:
        if m := re.search(_URI_PATTERN, uri):
            return cls(
                date=datetime.datetime.strptime(m.group("date"), "%Y-%m-%d").date(),
                studium=MotoStudium.from_name_en(m.group("studium_name_en")),
                race_no=int(m.group("race_no")),
            )
        else:
            return None

    @property
    def odds_source(self) -> OddsSource:
        return self.odds_source_type()(self)

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        from parimana.external.autorace.odds.scrape import MotoOddsSource

        return MotoOddsSource


_RACE_ID_PATTERN: re.Pattern = re.compile(
    r"MT(?P<date>[0-9]{8})(?P<studium_code>[0-9]{2})(?P<race_no>[0-9]{2})"
)

# ex1. https://autorace.jp/race_info/RaceResult/hamamatsu/2025-01-25_1
# ex2. https://autorace.jp/race_info/Live/hamamatsu/Odds/2025-01-25_9/rt3
_URI_PATTERN: re.Pattern = re.compile(
    r"autorace.jp/race_info/[^/]+/"
    r"(?P<studium_name_en>[a-z]{2,10})/"
    r"([^/]+/)?"
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})_"
    r"(?P<race_no>[0-9]{1,2})"
)


class _CategoryMoto(Category):

    def __init__(self):
        super().__init__(
            id="MT",
            name="オート",
            race_type=AutoRace,
            timezone=_moto_timezone,
            poll_start_time=datetime.time(hour=10, minute=10),
        )

    @property
    def schedule_source(self) -> ScheduleSource:
        from parimana.external.autorace.schedule.scrape import schedule_source

        return schedule_source


_moto_timezone = ZoneInfo("Asia/Tokyo")


category_moto = _CategoryMoto()
