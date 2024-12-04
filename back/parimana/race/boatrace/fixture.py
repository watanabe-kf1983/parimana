from dataclasses import dataclass

from parimana.race.fixture import (
    Course,
    FixtureSource,
    Category,
)


class BoatRaceCategory(Category):
    @property
    def id(self) -> str:
        return "bt"

    @property
    def name(self) -> str:
        return "ボートレース"

    @property
    def fixture_source(self) -> "FixtureSource":
        from parimana.race.boatrace.scrape_fixture import BoatFixtureSource

        return BoatFixtureSource()


@dataclass
class BoatRaceJo:
    jo_code: str
    name: str

    def to_fixture_course(self):
        return Course(
            id=f"bj{self.jo_code}", name=self.name, category=BoatRaceCategory()
        )
