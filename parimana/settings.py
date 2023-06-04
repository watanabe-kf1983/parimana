import argparse
from dataclasses import dataclass, field
from functools import cached_property
from typing import Sequence

from parimana.base.race import Race
from parimana.analyse.analyse import (
    Analyser,
    analysers,
    analyser_names,
    default_analyser_names,
)
from parimana.driver.chrome import headless_chrome
from parimana.boatrace.race import BoatRace
from parimana.netkeiba.race import NetKeibaRace


@dataclass(frozen=True)
class Settings:
    use_cache: bool = False
    simulation_count: int = 10_000_000
    race_type: str = "BOAT"
    boat_date: str = "20230531"
    boat_cource_id: int = 1
    boat_race_no: int = 12
    keiba_race_id: str = "202305021211"
    analyser_names: Sequence[str] = field(default_factory=default_analyser_names)

    @cached_property
    def race(self) -> Race:
        if self.race_type == "BOAT":
            return BoatRace(self.boat_date, self.boat_cource_id, self.boat_race_no)
        else:
            return NetKeibaRace(self.keiba_race_id, headless_chrome())

    @cached_property
    def analysers(self) -> Sequence[Analyser]:
        return [analysers[n] for n in self.analyser_names]

    @classmethod
    def from_cli_args(cls) -> "Settings":
        args = vars(_arg_parser().parse_args())
        return Settings(**args)


def _arg_parser() -> argparse.ArgumentParser:
    default_settings = Settings()
    parser = argparse.ArgumentParser(
        prog="parimana", description="Analyse pari-mutuel betting odds"
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        default=default_settings.use_cache,
        help="use odds cache once scraped",
    )
    parser.add_argument(
        "--analyser-names",
        choices=analyser_names,
        nargs="*",
        default=default_settings.analyser_names,
        help="using analyser",
    )
    parser.add_argument(
        "--simulation-count",
        type=int,
        default=default_settings.simulation_count,
        help="simulation sample number",
    )
    parser.add_argument(
        "--race-type",
        choices=["KEIBA", "BOAT"],
        default=default_settings.race_type,
        help="netkeiba as 'KEIBA' or boatrace.jp as 'BOAT'",
    )
    parser.add_argument(
        "--keiba-race-id",
        default=default_settings.keiba_race_id,
        help="netkeiba race_id",
    )
    parser.add_argument(
        "--boat-cource-id",
        type=int,
        default=default_settings.boat_cource_id,
        help="boat racecource id (kiryu=1)",
    )
    parser.add_argument(
        "--boat-date",
        default=default_settings.boat_date,
        help="boat datestr (yyyymmdd)",
    )
    parser.add_argument(
        "--boat-race-no",
        type=int,
        default=default_settings.boat_race_no,
        help="boat raceno (1~12)",
    )
    return parser
