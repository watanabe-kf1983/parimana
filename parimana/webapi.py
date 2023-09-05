from fastapi import FastAPI
import uvicorn

from parimana.settings import Settings
import parimana.batch as batch


app = FastAPI()


@app.post("/start-batch/")
def start_batch_process():
    task_id = batch.start_batch_process()
    return {"task_id": task_id}


@app.get("/get-result/{task_id}")
def get_batch_result(task_id: str):
    return batch.get_batch_result(task_id)


@app.post("/prepare")
def prepare(settings: Settings):
    task_id = batch.prepare(settings)
    return {"task_id": task_id}


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    start()
