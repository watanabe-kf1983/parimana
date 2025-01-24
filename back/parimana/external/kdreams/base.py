from dataclasses import dataclass
import datetime
import re
from typing import Mapping, Optional, Type
from zoneinfo import ZoneInfo

from parimana.domain.race import Race, OddsSource
from parimana.domain.schedule import Category, Fixture, ScheduleSource, Course


@dataclass
class KeirinStudium:
    code: str
    name: str
    name_en: str

    def to_course(self):
        return Course(id=f"kr{self.code}", name=self.name, category=category_keirin)

    @classmethod
    def from_code(cls, code: str):
        return _all_courses.get(code)


studium_list = (
    # https://keirin.kdreams.jp/stadium/?l-id=l-ti-directoryNav_link_stadium
    # https://ctc.gr.jp/link/
    "函館/hakodate/11 青森/aomori/12 いわき平/iwakitaira/13"
    " 弥彦/yahiko/21 前橋/maebashi/22 取手/toride/23 宇都宮/utsunomiya/24"
    " 大宮/omiya/25 西武園/seibuen/26 京王閣/keiokaku/27 立川/tachikawa/28"
    " 松戸/matsudo/31 川崎/kawasaki/34 平塚/hiratsuka/35"
    " 小田原/odawara/36 伊東/ito/37 静岡/shizuoka/38"
    " 名古屋/nagoya/42 岐阜/gifu/43 大垣/ogaki/44 豊橋/toyohashi/45"
    " 富山/toyama/46 松阪/matsusaka/47 四日市/yokkaichi/48"
    " 福井/fukui/51 奈良/nara/53 向日町/mukomachi/54 和歌山/wakayama/55 岸和田/kishiwada/56"
    " 玉野/tamano/61 広島/hiroshima/62 防府/hofu/63"
    " 高松/takamatsu/71 小松島/komatsushima/73 高知/kochi/74 松山/matsuyama/75"
    " 小倉/kokura/81 久留米/kurume/83 武雄/takeo/84 佐世保/sasebo/85 別府/beppu/86 熊本/kumamoto/87"
)


_all_courses: Mapping[str, KeirinStudium] = {
    code: KeirinStudium(code, name, name_en)
    for name, name_en, code in (studium.split("/") for studium in studium_list.split())
}


@dataclass
class Meeting:
    studium: KeirinStudium
    first_day: datetime.date

    @property
    def code(self):
        return f"{self.studium.code}{self.first_day:%Y%m%d}"

    @classmethod
    def from_codes(cls, studium_code: str, first_day: str):
        return cls(
            KeirinStudium.from_code(studium_code),
            datetime.datetime.strptime(first_day, "%Y%m%d"),
        )

    @classmethod
    def from_code(cls, code: str) -> "Meeting":
        if m := re.fullmatch(_MEETING_PATTERN, code):
            return cls.from_codes(**m.groupdict())
        else:
            return ValueError(f"Invalid code {code}")


_MEETING_PATTERN: re.Pattern = re.compile(
    r"(?P<studium_code>[0-9]{2})(?P<first_day>[0-9]{8})"
)


@dataclass
class MeetingDay:
    meeting: Meeting
    day_num: int

    @property
    def code(self) -> str:
        return f"{self.meeting.code}{self.day_num:02}00"

    @property
    def date(self) -> datetime.date:
        return self.meeting.first_day + datetime.timedelta(days=self.day_num - 1)

    def to_fixture(self) -> Fixture:
        return Fixture(date=self.date, course=self.meeting.studium.to_course())

    @classmethod
    def from_codes(cls, meeting_code: str, day_num_code: str):
        return cls(Meeting.from_code(meeting_code), int(day_num_code))

    @classmethod
    def from_code(cls, code: str) -> "MeetingDay":
        if m := re.fullmatch(_MEETING_DAY_PATTERN, code):
            return cls.from_codes(**m.groupdict())
        else:
            return ValueError(f"Invalid code {code}")


_MEETING_DAY_PATTERN: re.Pattern = re.compile(
    r"(?P<meeting_code>[0-9]{10})(?P<day_num_code>[0-9]{2})00"
)


@dataclass
class KeirinRace(Race):
    meeting_day: MeetingDay
    race_no: int

    @property
    def race_id(self) -> str:
        return f"kr{self.code}"

    @property
    def name(self) -> str:
        return f"{self.race_no}R"

    @property
    def code(self):
        return f"{self.meeting_day.code}{self.race_no:02}"

    @property
    def odds_source(self) -> OddsSource:
        return self.odds_source_type()(self)

    @classmethod
    def odds_source_type(cls) -> Type[OddsSource]:
        from parimana.external.kdreams.odds.scrape import KeirinOddsSource

        return KeirinOddsSource

    @classmethod
    def from_codes(cls, meeting_day_code: str, race_no: str) -> "KeirinRace":
        return cls(MeetingDay.from_code(meeting_day_code), int(race_no))

    @classmethod
    def from_code(cls, code: str) -> "KeirinRace":
        if m := re.fullmatch(_RACE_CODE_PATTERN, code):
            return cls.from_codes(**m.groupdict())
        else:
            return ValueError(f"Invalid code {code}")

    @classmethod
    def from_id(cls, race_id: str) -> Optional["KeirinRace"]:
        if m := re.fullmatch(_RACE_ID_PATTERN, race_id):
            return cls.from_code(**m.groupdict())
        else:
            return None

    @classmethod
    def from_uri(cls, uri: str) -> Optional["KeirinRace"]:
        if "keirin.kdreams.jp" not in uri:
            return None

        if m := re.search(_URI_RACE_ID_PATTERN, uri):
            return cls.from_code(**m.groupdict())
        else:
            return None


_RACE_CODE_PATTERN: re.Pattern = re.compile(
    r"(?P<meeting_day_code>[0-9]{14})(?P<race_no>[0-9]{2})"
)
_RACE_ID_PATTERN: re.Pattern = re.compile(r"kr(?P<code>[0-9]{16})")
_URI_RACE_ID_PATTERN: re.Pattern = re.compile(r"racedetail/(?P<code>[0-9]{16})/")


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
        from parimana.external.kdreams.schedule.scrape import schedule_source

        return schedule_source


_keirin_timezone = ZoneInfo("Asia/Tokyo")


category_keirin = _CategoryKeirin()
