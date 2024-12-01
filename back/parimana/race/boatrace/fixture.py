from parimana.race.fixture import (
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
