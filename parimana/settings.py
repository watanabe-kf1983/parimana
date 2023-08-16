import argparse
from dataclasses import dataclass, field
from functools import cached_property
from typing import Collection, Sequence, Type

from parimana.base.race import Race
from parimana.analyse.analyse import (
    Analyser,
    analysers,
    analyser_names,
    default_analyser_names,
)
from parimana.boatrace.race import BoatRace
from parimana.netkeiba.race import NetKeibaRace


@dataclass(frozen=True)
class Settings:
    race_id: str
    use_cache: bool = False
    simulation_count: int = 10_000_000
    analyser_names: Sequence[str] = field(default_factory=default_analyser_names)
    recommend_query: str = ""
    recommend_size: int = 20

    @cached_property
    def race(self) -> Race:
        race_types: Collection[Type[Race]] = [BoatRace, NetKeibaRace]

        for race_type in race_types:
            if found := race_type.from_race_id(self.race_id):
                return found

        raise ValueError(f"race_id: {self.race_id} is illegal")

    @cached_property
    def analysers(self) -> Sequence[Analyser]:
        return [analysers[n] for n in self.analyser_names]

    @classmethod
    def from_cli_args(cls) -> "Settings":
        args = vars(_arg_parser().parse_args())
        return Settings(**args)


def _arg_parser() -> argparse.ArgumentParser:
    default_settings = Settings("")
    parser = argparse.ArgumentParser(
        prog="parimana", description="Analyse pari-mutuel betting odds"
    )
    parser.add_argument(
        "race_id",
        type=str,
        help=(
            "'boatrace-{YYYYMMDD}-{JCD}-{RACE_NO}' or 'netkeiba-{NETKEIBA_RACE_ID}' \n"
            "  (ex: boatrace-20230531-1-12, netkeiba-202305021211)"
        ),
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        default=default_settings.use_cache,
        help="use odds cache once scraped",
    )
    parser.add_argument(
        "-a",
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
        "-q",
        "--recommend-query",
        type=str,
        default=default_settings.recommend_query,
        help=(
            "query string to filter recommendation. \n"
            " (ex: \"type == 'TRIFECTA' and expected >= 120\")"
        ),
    )
    parser.add_argument(
        "-s",
        "--recommend-size",
        type=int,
        default=default_settings.recommend_size,
        help=("maximum number of candidates to recommend."),
    )
    return parser
