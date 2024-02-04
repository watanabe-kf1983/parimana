import os
from enum import Enum
import time
from typing import Sequence

from celery import Celery, chain, group

from parimana.analyse import analysers, AnalysisResult
from parimana.app.status import ProcessStatusManager
from parimana.race import Race, RaceOddsPool, RaceSelector
from parimana.repository import FileRepository
from parimana.app.settings import Settings

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

app = Celery(
    __name__, 
    backend=f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/0",
    broker=f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/0"
)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]

repo = FileRepository()


class ProcessStatus(str, Enum):
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    NOT_STARTED = "NOT_STARTED"


@app.task
def get_odds_pool(race: Race, scrape_force: bool = False) -> RaceOddsPool:
    odds_pool = repo.load_latest_odds_pool(race)

    if odds_pool and (odds_pool.timestamp.is_confirmed or not scrape_force):
        return odds_pool
    else:
        timestamp = race.source.scrape_odds_timestamp()
        if (not odds_pool) or odds_pool.timestamp < timestamp:
            odds_pool = race.source.scrape_odds_pool()
            repo.save_odds_pool(odds_pool)
        return odds_pool


@app.task
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int
) -> AnalysisResult:
    charts = repo.load_charts(odds_pool.race, odds_pool.timestamp, analyser_name)

    if charts:
        return charts.result
    else:
        r = analysers[analyser_name].analyse(odds_pool, simulation_count)
        repo.save_charts(odds_pool.race, odds_pool.timestamp, r.get_charts())
        return r


@app.task
def finish_process(results=None, /, *, race):
    ProcessStatusManager(race).finish_process()
    return results


@app.task
def start_process(race):
    ProcessStatusManager(race).start_process()


def get_analysis(settings: Settings):
    race = RaceSelector.select(settings.race_id)
    return chain(
        start_process.s(race=race),
        get_odds_pool.si(race, not settings.use_cache),
        group(
            analyse.s(analyser_name, settings.simulation_count)
            for analyser_name in settings.analyser_names
        ),
        finish_process.s(race=race),
    )


@app.task
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