# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

import argparse
from dataclasses import dataclass, field
from typing import Sequence

from parimana.analyse import (
    analyser_names,
    default_analyser_names,
)


@dataclass(frozen=True)
class Settings:
    race_id: str
    use_cache: bool = False
    simulation_count: int = 10_000_000
    analyser_names: Sequence[str] = field(default_factory=default_analyser_names)
    recommend_query: str = ""
    recommend_size: int = 20

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
            "'bt{YYYYMMDD}{JCD}{RACE_NO}' or 'hr{NETKEIBA_RACE_ID}' \n"
            "  (ex: bt202305310112, hr202305021211)"
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
