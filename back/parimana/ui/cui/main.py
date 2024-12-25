from typing import Sequence

import parimana.tasks as tasks
from parimana.ui.cui.argparse import parse_analyse_options


def update_schedule() -> None:
    tasks.update_schedule_all().apply()


def main():
    options = parse_analyse_options()
    results = tasks.scrape_and_analyse(options).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(options.recommend_query, options.recommend_size)
