from fastapi import FastAPI
import uvicorn

from parimana.settings import Settings
import parimana.batch as batch


app = FastAPI()


@app.post("/start-wait-30/")
def start_wait_30():
    task_id = batch.start_wait_30()
    return {"task_id": task_id}


@app.get("/wait-30-result/{task_id}")
def get_wait_30_result(task_id: str):
    return batch.get_wait_30_result(task_id)


@app.post("/start-analyse")
def start_analyse(settings: Settings):
    task_id = batch.start_analyse(settings)
    return {"task_id": task_id}


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    start()
