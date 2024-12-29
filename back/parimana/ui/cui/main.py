from typing import Sequence

from parimana import settings
from parimana.app.analyse import AnalyseApp
from parimana.app.collect_odds import OddsCollectorApp
from parimana.app.schedule import ScheduleApp
from parimana.app.status import ProcessStatusManager
from parimana.domain.race import RaceSelector

import parimana.tasks as tasks
from parimana.ui.cui.argparse import parse_analyse_options


schedule_tasks = tasks.ScheduleTasks(
    schedule_app=ScheduleApp(
        categories=settings.categories, store=settings.schedule_storage
    ),
)

analyse_tasks = tasks.AnalyseTasks(
    analyse_app=AnalyseApp(store=settings.analysis_storage),
    odds_app=OddsCollectorApp(store=settings.odds_storage),
    ps_manager=ProcessStatusManager(
        store=settings.status_storage, center=settings.publish_center
    ),
    race_selector=RaceSelector(settings.race_types),
)


def update_schedule() -> None:
    schedule_tasks.update_schedule_all().apply()


def main():
    options = parse_analyse_options()
    results = analyse_tasks.scrape_and_analyse(options).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(options.recommend_query, options.recommend_size)


def run_worker():
    tasks.run_worker()
