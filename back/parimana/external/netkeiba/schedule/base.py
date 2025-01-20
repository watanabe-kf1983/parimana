from abc import ABC, abstractmethod
from dataclasses import dataclass

from parimana.domain.schedule import Course
from parimana.external.netkeiba.base import category_jra, category_nar


@dataclass
class NetKeibaCourse(ABC):
    code: str
    name: str

    @abstractmethod
    def to_course(self):
        pass

    @classmethod
    def from_code(cls, code: str) -> "NetKeibaCourse":
        raise NotImplementedError()


@dataclass
class JraCourse(NetKeibaCourse):
    def to_course(self):
        return Course(id=f"hj{self.code}", name=self.name, category=category_jra)

    @classmethod
    def from_code(cls, code: str) -> "JraCourse":
        return _all_jra_courses.get(code)


@dataclass
class NarCourse(NetKeibaCourse):
    def to_course(self):
        return Course(id=f"hn{self.code}", name=self.name, category=category_nar)

    @classmethod
    def from_code(cls, code: str) -> "NarCourse":
        return _all_nar_courses.get(code)


# https://www.jra.go.jp/dento/member/manual/pdf/ars/code.pdf
_all_jra_courses = {
    code: JraCourse(code, name)
    for name, code in (
        course_text.split("/")
        for course_text in (
            "札幌/01 函館/02 福島/03 新潟/04 東京/05"
            " 中山/06 中京/07 京都/08 阪神/09 小倉/10"
        ).split()
    )
}


# https://nar.netkeiba.com/racecourse/racecourse_list.html?rf=sidemenu
_all_nar_courses = {
    code: NarCourse(code, name)
    for name, code in (
        course_text.split("/")
        for course_text in (
            "帯広/65 門別/30 盛岡/35 水沢/36 浦和/42"
            " 船橋/43 大井/44 川崎/45 金沢/46 笠松/47"
            " 名古屋/48 園田/50 姫路/51 高知/54 佐賀/55"
        ).split()
    )
}
