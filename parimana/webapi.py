from fastapi import FastAPI
import uvicorn

from parimana.batch import batch_process

app = FastAPI()

@app.post("/start-batch/")
def start_batch_process():
    task = batch_process.delay("input_data")
    return {"task_id": task.id}


@app.get("/get-result/{task_id}")
def get_batch_result(task_id: str):
    task = batch_process.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": task.state, "result": task.result}
    else:
        return {"status": task.state}


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")

if __name__ == "__main__":
    start()
    