from dataclasses import dataclass

from parimana.race.schedule import Course
from parimana.race.netkeiba.base import category_keiba


@dataclass
class JraCourse:
    code: str
    name: str

    def to_course(self):
        return Course(id=f"hr{self.code}", name=self.name, category=category_keiba)

    @classmethod
    def from_code(cls, code: str):
        return _all_courses.get(code)


# https://www.jra.go.jp/dento/member/manual/pdf/ars/code.pdf
_all_courses = {
    code: JraCourse(code, name)
    for name, code in (
        course_text.split("/")
        for course_text in (
            "札幌/01 函館/02 福島/03 新潟/04 東京/05 "
            "中山/06 中京/07 京都/08 阪神/09 小倉/10"
        ).split()
    )
}
