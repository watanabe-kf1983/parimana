from pathlib import Path
import time
from typing import Mapping

from celery import Celery

from parimana.analyse.analyse import Analyser, AnalysisResult
from parimana.base.race import Race
from parimana.settings import Settings
from parimana.storage.race_manager import RaceManager

app = Celery(
    __name__, backend="redis://localhost:6379/0", broker="redis://localhost:6379/0"
)


@app.task
def batch_process(data):
    # バッチ処理の実装
    # 処理が終了したら結果を返すか、DBに保存するなど
    time.sleep(30)
    result = "Batch processing completed"
    return result


@app.task(ignore_result=True)
def analyse(race: Race, simulation_count: int, analyser: Analyser, dir: Path) -> None:
    analyser.analyse(race, simulation_count).save(dir / analyser.name)


@app.task
def get_race(rm: RaceManager, scrape_force: bool = False) -> None:
    rm.get_race(scrape_force)


def main(settings: Settings) -> Mapping[str, AnalysisResult]:
    rm = RaceManager(settings.race_id)
    race = rm.get_race(force_scrape=not settings.use_cache)

    results = {}
    for a in settings.analysers:
        r = a.analyse(race=race, simulation_count=settings.simulation_count)
        r.save(rm.base_dir / a.name)
        results[a.name] = r
    return results
