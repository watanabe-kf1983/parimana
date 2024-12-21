from typing import Sequence

import parimana.tasks as tasks
import parimana.settings as settings
from parimana.ui.cui.argparse import parse_analyse_options


def scrape_schedule() -> None:
    for cat in settings.categories:
        sc = tasks.get_schedule.s(cat=cat).apply().get()
        print(sc)


def main():
    options = parse_analyse_options()
    results = tasks.scrape_and_analyse(options).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(options.recommend_query, options.recommend_size)

