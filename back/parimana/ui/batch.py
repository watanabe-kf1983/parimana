from typing import Sequence
from functools import wraps
import traceback

from celery import Celery, chain, group

import parimana.infra.message as msg
from parimana.domain.analyse import AnalysisResult
from parimana.domain.race import Race, RaceOddsPool
from parimana.domain.schedule import Category, RaceInfo
from parimana.app.analyse import AnalyseApp
from parimana.app.schedule import ScheduleApp
from parimana.app.status import ProcessStatusManager
from parimana.devices.file import FileRepository
from parimana.ui.settings import Settings, race_selector, category_selector

app = Celery(__name__, backend=msg.uri, broker=msg.uri)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]

repo = FileRepository()


def with_race_channel(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "race" in kwargs:
            channel_id = kwargs["race"].race_id
        else:
            channel_id = None

        with msg.set_printer(channel_id) as p:
            try:
                return func(*args, **kwargs)
            except Exception:
                p.mprint("ERROR occurred:")
                stack_trace = traceback.format_exc()
                p.mprint(stack_trace)
                ProcessStatusManager(repo, kwargs["race"]).abort_process()
                raise

    return wrapper


@app.task
def get_schedule(*, cat: Category) -> Sequence[RaceInfo]:
    return ScheduleApp(repo).scrape_and_get_schedule(cat)


@app.task
@with_race_channel
def get_odds_pool(*, race: Race, scrape_force: bool = False) -> RaceOddsPool:
    return AnalyseApp(repo).get_odds_pool(race, scrape_force)


@app.task
@with_race_channel
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int, *, race: Race
) -> AnalysisResult:
    return AnalyseApp(repo).analyse(odds_pool, analyser_name, simulation_count)


@app.task
@with_race_channel
def finish_process(results=None, /, *, race: Race):
    ProcessStatusManager(repo, race).finish_process()
    msg.mclose()
    return results


@app.task
@with_race_channel
def start_process(*, race: Race):
    ProcessStatusManager(repo, race).start_process()


def get_analysis(settings: Settings):
    race = race_selector.select(settings.race_id)
    return chain(
        start_process.s(race=race),
        get_odds_pool.si(race=race, scrape_force=not settings.use_cache),
        group(
            analyse.s(analyser_name, settings.simulation_count, race=race)
            for analyser_name in settings.analyser_names
        ),
        finish_process.s(race=race),
    )


def start_analyse(settings: Settings) -> str:
    return get_analysis(settings).delay().id


def main():
    settings = Settings.from_cli_args()

    results = get_analysis(settings).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(settings.recommend_query, settings.recommend_size)


def run_worker():
    app.worker_main(argv=["worker", "-P", "threads", "--loglevel=info"])


if __name__ == "__main__":
    for cat in category_selector.all():
        sc = get_schedule.s(cat=cat).apply().get()
        print(sc)
