from celery import chain, group
from fastapi import FastAPI
import uvicorn

from parimana.settings import Settings
from parimana.storage.race_manager import RaceManager
import parimana.batch as batch


app = FastAPI()


@app.post("/start-batch/")
def start_batch_process():
    task = batch.batch_process.delay("input_data")
    return {"task_id": task.id}


@app.get("/get-result/{task_id}")
def get_batch_result(task_id: str):
    task = batch.batch_process.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": task.state, "result": task.result}
    else:
        return {"status": task.state}


@app.post("/prepare")
def prepare_async(settings: Settings):
    rm = RaceManager(settings.race_id)
    chain(
        batch.get_race.s(rm=rm, force=not settings.use_cache),
        group(
            batch.analyse.s(settings.simulation_count, analyser, rm.base_dir)
            for analyser in settings.analysers
        ).delay(),
    )


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    start()
