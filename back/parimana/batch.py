from pathlib import Path
import time
from typing import Sequence

from celery import Celery, chain, group

from parimana.base.odds_pool import RaceOddsPool
from parimana.base.race import Race
from parimana.race import get_race
from parimana.analyse.analyse import AnalysisResult, analysers
from parimana.race.select import get_race_source
from parimana.repository.file_repository import FileRepository
from parimana.settings import Settings

app = Celery(
    __name__, backend="redis://localhost:6379/0", broker="redis://localhost:6379/0"
)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]

repo = FileRepository(Path(".output"))


@app.task
def get_odds_pool(race: Race, scrape_force: bool = False) -> RaceOddsPool:
    odds_pool = repo.load_latest_odds_pool(race)

    if odds_pool and (odds_pool.timestamp.is_confirmed or not scrape_force):
        return odds_pool
    else:
        odds_pool = get_race_source(race).scrape_odds_pool()
        repo.save_odds_pool(odds_pool)
        return odds_pool


@app.task
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int
) -> AnalysisResult:
    r = analysers[analyser_name].analyse(odds_pool, simulation_count)
    repo.save_charts(r.get_charts())
    return r


def get_analysis(settings: Settings):
    race = get_race(settings.race_id)
    return chain(
        get_odds_pool.s(race, not settings.use_cache),
        group(
            analyse.s(analyser_name, settings.simulation_count)
            for analyser_name in settings.analyser_names
        ),
    )


@app.task
def wait_30_seconds(data):
    time.sleep(30)
    result = data + ": waited_30_seconds"
    return result


def main(settings: Settings) -> Sequence[AnalysisResult]:
    result = get_analysis(settings).apply().get()
    return result if isinstance(result, Sequence) else [result]


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
