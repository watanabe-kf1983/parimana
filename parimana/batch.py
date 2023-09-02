from typing import Mapping
import time

from celery import Celery

from parimana.analyse.analyse import AnalysisResult
from parimana.settings import Settings


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



def main(settings: Settings) -> Mapping[str, AnalysisResult]:
    race = settings.race
    if not settings.use_cache:
        race.remove_odds_cache()

    results = {}
    for a in settings.analysers:
        r = a.analyse(race=race, simulation_count=settings.simulation_count)
        r.save(race.base_dir / a.name)
        results[a.name] = r
    return results
