from dataclasses import dataclass
from datetime import date
import datetime
from typing import Optional
import re


RACE_ID_PATTERN: re.Pattern = re.compile(
    r"bt"
    r"(?P<date>[0-9]{8})"
    r"(?P<course_id>[0-9a-zA-Z]{2})"
    r"(?P<race_no>[0-9]{2})"
)


@dataclass
class RaceIdElements:
    date: date
    course_id: str
    race_no: int

    def generate_id(self) -> str:
        return f"bt{self.date:%Y%m%d}{self.course_id}{self.race_no:02}"

    @classmethod
    def parse_from_id(cls, race_id: str) -> Optional["RaceIdElements"]:
        if m := re.fullmatch(RACE_ID_PATTERN, race_id):
            parsed = m.groupdict()
            return cls(
                date=datetime.datetime.strptime(parsed["date"], "%Y%m%d").date(),
                course_id=parsed["course_id"],
                race_no=int(parsed["race_no"]),
            )
        else:
            return None
