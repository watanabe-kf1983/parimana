import datetime
from enum import Enum
import time
from typing import Mapping, Sequence
from functools import wraps
import traceback

from celery import Celery, chain, group

from parimana.analyse import analysers, AnalysisResult
from parimana.app.status import ProcessStatusManager
from parimana.app.settings import Settings
from parimana.race import Race, RaceOddsPool, RaceSelector, CategorySelector
from parimana.race.schedule import Category, RaceSchedule
from parimana.repository import FileRepository
import parimana.message as msg

app = Celery(__name__, backend=msg.uri, broker=msg.uri)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]

repo = FileRepository()


class ProcessStatus(str, Enum):
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    NOT_STARTED = "NOT_STARTED"


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
                ProcessStatusManager(kwargs["race"]).abort_process()
                raise

    return wrapper


# def with_channel(channel_id: str):

#     def with_channel_w(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):

#             with msg.set_printer(channel_id) as p:
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception:
#                     p.mprint("ERROR occurred:")
#                     stack_trace = traceback.format_exc()
#                     p.mprint(stack_trace)
#                     raise

#         return wrapper

#     return with_channel_w


@app.task
def get_schedule(*, cat: Category) -> Mapping[datetime.date, Sequence[RaceSchedule]]:

    schedule = repo.load_schedule(cat)

    if schedule and (datetime.date.today() in schedule):
        return schedule
    else:
        schedule = cat.schedule_source.scrape()
        repo.save_schedule(cat, schedule)
        return schedule


@app.task
@with_race_channel
def get_odds_pool(*, race: Race, scrape_force: bool = False) -> RaceOddsPool:
    odds_pool = repo.load_latest_odds_pool(race)

    if odds_pool and (odds_pool.timestamp.is_confirmed or not scrape_force):
        return odds_pool
    else:
        timestamp = race.odds_source.scrape_timestamp()
        if (not odds_pool) or odds_pool.timestamp < timestamp:
            odds_pool = race.odds_source.scrape_odds_pool()
            repo.save_odds_pool(odds_pool)
        return odds_pool


@app.task
@with_race_channel
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int, *, race: Race
) -> AnalysisResult:
    charts = repo.load_charts(odds_pool.race, odds_pool.timestamp, analyser_name)

    if charts:
        return charts.result
    else:
        r = analysers[analyser_name].analyse(odds_pool, simulation_count)
        repo.save_charts(odds_pool.race, odds_pool.timestamp, r.get_charts())
        return r


@app.task
@with_race_channel
def finish_process(results=None, /, *, race: Race):
    ProcessStatusManager(race).finish_process()
    msg.mclose()
    return results


@app.task
@with_race_channel
def start_process(*, race: Race):
    ProcessStatusManager(race).start_process()


def get_analysis(settings: Settings):
    race = RaceSelector.select(settings.race_id)
    return chain(
        start_process.s(race=race),
        get_odds_pool.si(race=race, scrape_force=not settings.use_cache),
        group(
            analyse.s(analyser_name, settings.simulation_count, race=race)
            for analyser_name in settings.analyser_names
        ),
        finish_process.s(race=race),
    )


@app.task
@with_race_channel
def wait_30_seconds(data):
    time.sleep(30)
    result = data + ": waited_30_seconds"
    return result


def start_analyse(settings: Settings) -> str:
    return get_analysis(settings).delay().id


def start_wait_30() -> str:
    return wait_30_seconds.delay("input_data").id


def get_wait_30_result(task_id: str):
    task = wait_30_seconds.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": task.state, "result": task.result}
    else:
        return {"status": task.state}


def main():
    settings = Settings.from_cli_args()

    results = get_analysis(settings).apply().get()

    results = results if isinstance(results, Sequence) else [results]
    for result in results:
        result.print_recommendation(settings.recommend_query, settings.recommend_size)


def run_worker():
    app.worker_main(argv=["worker", "-P", "threads", "--loglevel=info"])


if __name__ == "__main__":
    cat = CategorySelector.select("bt")
    sc = get_schedule.s(cat=cat).apply().get()
    print(sc)
