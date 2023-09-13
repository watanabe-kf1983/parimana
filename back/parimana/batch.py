import time
from typing import Sequence

from celery import Celery, chain, group

from parimana.base.race import RaceOddsPool
from parimana.settings import Settings
from parimana.analyse.analyse import AnalysisResult, analysers
from parimana.storage.race_manager import RaceManager

app = Celery(
    __name__, backend="redis://localhost:6379/0", broker="redis://localhost:6379/0"
)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]


@app.task
def get_odds_pool(rm: RaceManager, scrape_force: bool = False) -> RaceOddsPool:
    return rm.get_odds_pool(scrape_force)


@app.task
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int
) -> AnalysisResult:
    r = analysers[analyser_name].analyse(odds_pool, simulation_count)
    r.save(RaceManager(odds_pool.race_id).base_dir / analyser_name)
    return r


def get_analysis(settings: Settings):
    return chain(
        get_odds_pool.s(RaceManager(settings.race_id), not settings.use_cache),
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
