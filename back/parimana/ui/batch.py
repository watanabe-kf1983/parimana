from typing import Sequence

from celery import Celery, chain, group

import parimana.infra.message as msg
from parimana.domain.analyse import AnalysisResult
from parimana.domain.race import Race, RaceOddsPool
from parimana.domain.schedule import Category, RaceInfo
from parimana.app.analyse import AnalyseApp
from parimana.app.schedule import ScheduleApp
from parimana.app.status import ProcessStatusManager
from parimana.ui.settings import Settings, category_selector, race_selector, repo

app = Celery(__name__, backend=msg.uri, broker=msg.uri)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]

schedule_app = ScheduleApp(repo.schedule)
analyse_app = AnalyseApp(repo.analysis)
ps_manager = ProcessStatusManager(repo.status)


@app.task
def get_schedule(*, cat: Category) -> Sequence[RaceInfo]:
    return schedule_app.scrape_and_get_schedule(cat)


@app.task
@msg.with_channel_printer
def get_odds_pool(*, race: Race, scrape_force: bool = False) -> RaceOddsPool:
    return analyse_app.get_odds_pool(race=race, scrape_force=scrape_force)


@app.task
@msg.with_channel_printer
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int
) -> AnalysisResult:
    return analyse_app.analyse(odds_pool, analyser_name, simulation_count)


@app.task
@msg.with_channel_printer
def start_process(*, process_name: str):
    ps_manager.start_process(process_name)


@app.task
@msg.with_channel_printer
def finish_process(results=None, /, *, process_name: str):
    ps_manager.finish_process(process_name)
    return results


@app.task
@msg.with_channel_printer
def handle_error(request, exc, traceback, *, process_name: str):
    msg.mprint("ERROR occurred:")
    msg.mprint(exc)
    msg.mprint(traceback)
    msg.mprint(f"Failed task info: args={request.args}, kwargs={request.kwargs}, ")
    msg.mprint("")
    ps_manager.abort_process(process_name)


def get_analysis(settings: Settings):
    race = race_selector.select(settings.race_id)
    process_name = f"analyse_{settings.race_id}"
    return chain(
        start_process.s(channel_id=process_name, process_name=process_name),
        get_odds_pool.si(
            race=race, channel_id=process_name, scrape_force=not settings.use_cache
        ),
        group(
            analyse.s(analyser_name, settings.simulation_count, channel_id=process_name)
            for analyser_name in settings.analyser_names
        ),
        finish_process.s(channel_id=process_name, process_name=process_name),
    ).on_error(handle_error.s(channel_id=process_name, process_name=process_name))


def start_analyse(settings: Settings) -> str:
    return get_analysis(settings).delay().id


def scrape_schedule() -> None:
    for cat in category_selector.all():
        sc = get_schedule.s(cat=cat).apply().get()
        msg.mprint(sc)
        msg.mclose()


def main():
    settings = Settings.from_cli_args()

    results = get_analysis(settings).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(settings.recommend_query, settings.recommend_size)


def run_worker():
    app.worker_main(argv=["worker", "--concurrency=1", "--loglevel=info"])


if __name__ == "__main__":
    scrape_schedule()
