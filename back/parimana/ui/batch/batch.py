from typing import Sequence

from celery import Celery, chain, group

from parimana.infra.message import mprint, mclose
from parimana.domain.analyse import AnalysisResult
from parimana.domain.race import Race, RaceOddsPool
from parimana.domain.schedule import Category, RaceInfo
from parimana.app.analyse import AnalyseApp
from parimana.app.schedule import ScheduleApp
from parimana.app.status import ProcessStatusManager
from parimana.ui.batch.options import CuiOptions
import parimana.settings as settings

app = Celery(
    __name__, backend=settings.task_backend_uri, broker=settings.task_broker_uri
)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]

schedule_app = ScheduleApp(
    categories=settings.categories, repo=settings.schedule_repository
)
analyse_app = AnalyseApp(
    race_types=settings.race_types, repo=settings.analysis_repository
)
ps_manager = ProcessStatusManager(settings.status_repository)

with_channel_printer = settings.publish_center.with_channel_printer


@app.task
def get_schedule(*, cat: Category) -> Sequence[RaceInfo]:
    return schedule_app.scrape_and_get_schedule(cat)


@app.task
@with_channel_printer
def get_odds_pool(*, race: Race, scrape_force: bool = False) -> RaceOddsPool:
    return analyse_app.get_odds_pool(race=race, scrape_force=scrape_force)


@app.task
@with_channel_printer
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int
) -> AnalysisResult:
    return analyse_app.analyse(odds_pool, analyser_name, simulation_count)


@app.task
@with_channel_printer
def start_process(*, process_name: str):
    ps_manager.start_process(process_name)


@app.task
@with_channel_printer
def finish_process(results=None, /, *, process_name: str):
    ps_manager.finish_process(process_name)
    return results


@app.task
@with_channel_printer
def handle_error(request, exc, traceback, *, process_name: str):
    mprint("ERROR occurred:")
    mprint(exc)
    mprint(traceback)
    mprint(f"Failed task info: args={request.args}, kwargs={request.kwargs}, ")
    mprint("")
    ps_manager.abort_process(process_name)


def get_analysis(options: CuiOptions):
    race = analyse_app.select_race(options.race_id)
    process_name = f"analyse_{options.race_id}"
    return chain(
        start_process.s(channel_id=process_name, process_name=process_name),
        get_odds_pool.si(
            race=race, channel_id=process_name, scrape_force=not options.use_cache
        ),
        group(
            analyse.s(analyser_name, options.simulation_count, channel_id=process_name)
            for analyser_name in options.analyser_names
        ),
        finish_process.s(channel_id=process_name, process_name=process_name),
    ).on_error(handle_error.s(channel_id=process_name, process_name=process_name))


def start_analyse(options: CuiOptions) -> str:
    return get_analysis(options).delay().id


def scrape_schedule() -> None:
    for cat in settings.categories:
        sc = get_schedule.s(cat=cat).apply().get()
        mprint(sc)
        mclose()


def main():
    options = CuiOptions.from_cli_args()

    results = get_analysis(options).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(options.recommend_query, options.recommend_size)


def run_worker():
    app.worker_main(argv=["worker", "--concurrency=1", "--loglevel=info"])


if __name__ == "__main__":
    scrape_schedule()
