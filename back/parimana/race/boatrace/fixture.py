from dataclasses import dataclass
from datetime import date
import datetime
import itertools
from typing import Mapping, Optional, Sequence


from parimana.race.boatrace.race import BoatRace
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
                _create_schedule(date=date, boat_jo=boat_jo)
                for boat_jo in _boat_jo_map.values()
            ]
            for date in itertools.takewhile(
                lambda d: d < date_to,
                (date_from + datetime.timedelta(days=n) for n in itertools.count()),
            )
        }

    def find_race_info(cls, race_id: str) -> Optional[RaceInfo]:
        if race := BoatRace.from_id(race_id):
            return RaceInfo(
                race_id=race.race_id,
                name=f"{race.race_no:02}R",
                fixture=Fixture(
                    category=boatCategory,
                    course=_boat_jo_map[race.jo_code].to_fixture_course(),
                    date=race.date,
                ),
            )
        else:
            return None


boatCategory = Category(
    id="bt", name="ボートレース", fixture_source=BoatFixtureSource()
)


@dataclass
class BoatRaceJo:
    jo_code: str
    name: str

    def to_fixture_course(self):
        return Course(id=f"bj{self.jo_code}", name=self.name, category=boatCategory)


def generate_boat_jo_map() -> Mapping[str, BoatRaceJo]:

    # https://www.boatrace.jp/owpc/pc/extra/tb/support/guide/telephone.html
    jo_str_list = (
        "桐生#01 戸田#02 江戸川#03 平和島#04"
        " 多摩川#05 浜名湖#06 蒲郡#07 常滑#08"
        " 津#09 三国#10 びわこ#11 住之江#12"
        " 尼崎#13 鳴門#14 丸亀#15 児島#16"
        " 宮島#17 徳山#18 下関#19 若松#20"
        " 芦屋#21 福岡#22 唐津#23 大村#24"
    )

    map = {}

    for jo_str in jo_str_list.split(" "):
        name, jo_code = jo_str.split("#")
        map[jo_code] = BoatRaceJo(jo_code=jo_code, name=name)

    return map


_boat_jo_map = generate_boat_jo_map()


def _create_schedule(date: date, boat_jo: BoatRaceJo):
    fixture = Fixture(
        category=boatCategory, date=date, course=boat_jo.to_fixture_course()
    )
    return RaceSchedule(
        fixture=fixture,
        races=[
            RaceInfo(
                race_id=BoatRace(
                    date=date, jo_code=boat_jo.jo_code, race_no=race_no
                ).race_id,
                name=f"{race_no:02}R",
                fixture=fixture,
            )
            for race_no in range(1, 13)
        ],
    )
