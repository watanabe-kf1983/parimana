import time
from typing import Mapping

from celery import Celery, chain, group

from parimana.settings import Settings
from parimana.analyse.analyse import Analyser, AnalysisResult, analysers
from parimana.storage.race_manager import RaceManager

app = Celery(
    __name__, backend="redis://localhost:6379/0", broker="redis://localhost:6379/0"
)


@app.task(ignore_result=True)
def get_race(race_id: str, scrape_force: bool = False) -> None:
    rm: RaceManager = RaceManager(race_id)
    rm.get_race(scrape_force)


@app.task(ignore_result=True)
def analyse(race_id: str, simulation_count: int, analyser_name: str) -> AnalysisResult:
    rm: RaceManager = RaceManager(race_id)
    analyser: Analyser = analysers[analyser_name]
    r: AnalysisResult = analyser.analyse(rm.get_race(), simulation_count)
    r.save(rm.base_dir / analyser_name)
    return r


def prepare(settings: Settings):
    return chain(
        get_race.s(settings.race_id, not settings.use_cache),
        group(
            analyse.si(settings.race_id, settings.simulation_count, analyser_name)
            for analyser_name in settings.analyser_names
        ),
    )


@app.task
def batch_process(data):
    # バッチ処理の実装
    # 処理が終了したら結果を返すか、DBに保存するなど
    time.sleep(30)
    result = "Batch processing completed"
    return result


def main(settings: Settings) -> Mapping[str, AnalysisResult]:
    rm = RaceManager(settings.race_id)
    race = rm.get_race(force_scrape=not settings.use_cache)

    results = {}
    for a in settings.analysers:
        r = a.analyse(race=race, simulation_count=settings.simulation_count)
        r.save(rm.base_dir / a.name)
        results[a.name] = r
    return results


def main2(settings: Settings) -> Mapping[str, AnalysisResult]:
    return prepare(settings).apply().get()


def start_batch_process():
    task = batch_process.delay("input_data")
    return task.id


def get_batch_result(task_id: str):
    task = batch_process.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": task.state, "result": task.result}
    else:
        return {"status": task.state}
