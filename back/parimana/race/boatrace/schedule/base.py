from dataclasses import dataclass

from parimana.race.schedule import Course
from parimana.race.boatrace.base import category_boat


@dataclass
class BoatRaceJo:
    jo_code: str
    name: str

    def to_course(self):
        return Course(id=f"bj{self.jo_code}", name=self.name, category=category_boat)
