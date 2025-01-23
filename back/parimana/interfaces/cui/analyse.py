import argparse
from typing import Sequence

from parimana.domain.analyse.analysis_result import AnalysisResult
from parimana.tasks.analyse import AnalyseTaskOptions
from parimana.domain.analyse import analyser_names
from parimana.context import context as cx


def analyse(args):
    race_id_or_uri = args.pop("RACE_URL")
    race = cx.race_selector.select(race_id_or_uri)
    race_id = race.race_id

    cat = cx.category_selector.select_from_race(race)
    cx.schedule_tasks.scrape_race_info.s(cat=cat, race_id=race_id).apply().get()

    write_result: bool = args.pop("write_result")
    options = AnalyseTaskOptions(race_id=race_id, **args)
    got_results = cx.analyse_tasks.scrape_and_analyse(options).apply().get()
    results: Sequence[AnalysisResult] = (
        got_results if isinstance(got_results, Sequence) else [got_results]
    )
    for result in results:
        result.print_recommendation(options.recommend_query, options.recommend_size)
        if write_result:
            write_figures(race_id, result)


def write_figures(race_id: str, result: AnalysisResult):
    out = cx.output
    out.write_binary(
        f"{race_id}_{result.model.name}.xlsx",
        result.to_excel(),
    )
    out.write_text(
        f"{race_id}_{result.model.name}_chance.html",
        _fig_to_html(result.eev.chart().fig),
    )
    out.write_text(
        f"{race_id}_{result.model.name}_box_plot.html",
        _fig_to_html(result.model.plot_box()),
    )
    out.write_text(
        f"{race_id}_{result.model.name}_mds.html",
        _fig_to_html(result.model.plot_mds()),
    )


def _fig_to_html(fig) -> str:
    return fig.to_html(include_plotlyjs="cdn", include_mathjax="cdn")


def add_sub_parser(subparsers):
    default_options = AnalyseTaskOptions("")

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "analyse", help="analyse odds"
    )
    parser.set_defaults(func=analyse)
    parser.add_argument(
        "RACE_URL",
        type=str,
        help=(
            " Odds Page URL or Race ID\n"
            " (ex:"
            ' "https://www.boatrace.jp/owpc/pc/race/odds3t?rno=12&jcd=12&hd=20241222", '
            ' "https://race.netkeiba.com/odds/index.html?race_id=202305021211", '
            " bt202412221212, hj202305021211, etc. )"
        ),
    )
    parser.add_argument(
        "-w",
        "--write-result",
        action="store_true",
        default=False,
        help="write out result charts and excel",
    )
    parser.add_argument(
        "-u",
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
        "-c",
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
