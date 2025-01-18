from dataclasses import dataclass
from typing import Mapping

from parimana.domain.schedule import Course
from parimana.external.boatrace.base import category_boat


@dataclass
class BoatRaceJo:
    jo_code: str
    name: str

    def to_course(self):
        return Course(id=f"bj{self.jo_code}", name=self.name, category=category_boat)

    @classmethod
    def from_jo_code(cls, jo_code: str):
        return _all_courses.get(jo_code)


_all_courses: Mapping[str, BoatRaceJo] = {
    jo_code: BoatRaceJo(jo_code, name)
    for name, jo_code in (
        jo_str.split("/")
        for jo_str in (
            # https://web.archive.org/web/20240519113828/https://www.boatrace.jp/owpc/pc/extra/tb/support/guide/telephone.html
            "桐生/01 戸田/02 江戸川/03 平和島/04"
            " 多摩川/05 浜名湖/06 蒲郡/07 常滑/08"
            " 津/09 三国/10 びわこ/11 住之江/12"
            " 尼崎/13 鳴門/14 丸亀/15 児島/16"
            " 宮島/17 徳山/18 下関/19 若松/20"
            " 芦屋/21 福岡/22 唐津/23 大村/24"
        ).split()
    )
}
