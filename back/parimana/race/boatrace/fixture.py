from dataclasses import dataclass
from datetime import date
import datetime
import itertools
from typing import Mapping, Optional, Sequence


from parimana.race.boatrace.race_id import RaceIdElements
from parimana.race.fixture import (
    Course,
    Fixture,
    FixtureSource,
    Category,
    RaceInfo,
    RaceSchedule,
)


@dataclass
class BoatFixtureSource(FixtureSource):

    def scrape_calendar(
        self, date_from: Optional[date] = None, date_to: Optional[date] = None
    ) -> Mapping[date, Sequence[RaceSchedule]]:

        date_from = date_from or (datetime.date.today() + datetime.timedelta(days=-2))
        date_to = date_to or (datetime.date.today() + datetime.timedelta(days=2))
        return {
            date: [
                _create_schedule(date=date, course=course)
                for course in _course_map.values()
            ]
            for date in itertools.takewhile(
                lambda d: d < date_to,
                (date_from + datetime.timedelta(days=n) for n in itertools.count()),
            )
        }

    def find_race_info(cls, race_id: str) -> Optional[RaceInfo]:
        if e := RaceIdElements.parse_from_id(race_id):
            return RaceInfo(
                race_id=race_id,
                name=f"{e.race_no:02}R",
                fixture=Fixture(
                    category=boatCategory, course=_course_map[e.course_id], date=e.date
                ),
            )
        else:
            return None


def generate_course_map():

    # https://www.boatrace.jp/owpc/pc/extra/tb/support/guide/telephone.html
    course_list_str = (
        "桐生#01 戸田#02 江戸川#03 平和島#04"
        " 多摩川#05 浜名湖#06 蒲郡#07 常滑#08"
        " 津#09 三国#10 びわこ#11 住之江#12"
        " 尼崎#13 鳴門#14 丸亀#15 児島#16"
        " 宮島#17 徳山#18 下関#19 若松#20"
        " 芦屋#21 福岡#22 唐津#23 大村#24"
    )

    map = {}

    for course_str in course_list_str.split(" "):
        name, id = course_str.split("#")
        map[id] = Course(id=id, name=name, category=boatCategory)

    return map


boatCategory = Category(
    id="bt", name="ボートレース", fixture_source=BoatFixtureSource()
)
_course_map = generate_course_map()


def _create_schedule(date: date, course: Course):
    fixture = Fixture(category=boatCategory, date=date, course=course)
    return RaceSchedule(
        fixture=fixture,
        races=[
            RaceInfo(
                race_id=RaceIdElements(
                    date=date, course_id=course.id, race_no=race_no
                ).generate_id(),
                name=f"{race_no:02}R",
                fixture=fixture,
            )
            for race_no in range(1, 13)
        ],
    )
