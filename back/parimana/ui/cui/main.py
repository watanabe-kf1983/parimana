from typing import Sequence

from parimana.ui.cui.argparse import parse_analyse_options
import parimana.context as cx


def update_schedule() -> None:
    cx.schedule_tasks.update_schedule_all().apply()


def main():
    options = parse_analyse_options()
    results = cx.analyse_tasks.scrape_and_analyse(options).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(options.recommend_query, options.recommend_size)


def start_worker():
    cx.worker.start()


def start_monitor():
    cx.worker.start_monitor()
