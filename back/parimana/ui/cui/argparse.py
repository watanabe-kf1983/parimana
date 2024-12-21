import argparse

from parimana.domain.analyse import (
    analyser_names,
)
from parimana.tasks.analyse import AnalyseTaskOptions


def parse_analyse_options() -> AnalyseTaskOptions:
    args = vars(_arg_parser().parse_args())
    return AnalyseTaskOptions(**args)


def _arg_parser() -> argparse.ArgumentParser:
    default_options = AnalyseTaskOptions("")
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
        default=default_options.use_cache,
        help="use odds cache once scraped",
    )
    parser.add_argument(
        "-a",
        "--analyser-names",
        choices=analyser_names,
        nargs="*",
        default=default_options.analyser_names,
        help="using analyser",
    )
    parser.add_argument(
        "--simulation-count",
        type=int,
        default=default_options.simulation_count,
        help="simulation sample number",
    )
    parser.add_argument(
        "-q",
        "--recommend-query",
        type=str,
        default=default_options.recommend_query,
        help=(
            "query string to filter recommendation. \n"
            " (ex: \"type == 'TRIFECTA' and expected >= 120\")"
        ),
    )
    parser.add_argument(
        "-s",
        "--recommend-size",
        type=int,
        default=default_options.recommend_size,
        help=("maximum number of candidates to recommend."),
    )
    return parser
