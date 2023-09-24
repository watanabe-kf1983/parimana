from pathlib import Path
from typing import Optional, Sequence
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

import parimana.base
import parimana.analyse
from parimana.settings import Settings
from parimana.race import RaceSelector
import parimana.batch as batch
from parimana.repository.file_repository import FileRepository

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
    ],
)

repo = FileRepository(Path(".output"))


class Eye(BaseModel):
    text: str
    type: str

    @classmethod
    def from_base(cls, eye: parimana.base.Eye):
        return cls(text=eye.text, type=eye.type.name)


class EyeExpectedValue(BaseModel):
    eye: Eye
    odds: float
    chance: float
    expected: float

    @classmethod
    def from_base(cls, eev: parimana.analyse.EyeExpectedValue):
        return cls(
            eye=Eye.from_base(eev.eye),
            odds=eev.odds,
            chance=eev.chance,
            expected=eev.expected,
        )


@app.post("/start-wait-30/")
def start_wait_30():
    task_id = batch.start_wait_30()
    return {"task_id": task_id}


@app.get("/wait-30-result/{task_id}")
def get_wait_30_result(task_id: str):
    return batch.get_wait_30_result(task_id)


# @app.post("/start-analyse")
# def start_analyse(settings: Settings):
#     task_id = batch.start_analyse(settings)
#     return {"task_id": task_id}


@app.post("/start-analyse/{race_id}")
def start_analyse(race_id: str):
    settings = Settings(race_id, analyser_names=["no_cor", "ppf_mtx"])
    task_id = batch.start_analyse(settings)
    return {"task_id": task_id}


@app.get("/analysis/{race_id}/{analyser_name}")
def get_analysis(
    race_id: str, analyser_name: str
) -> Optional[Sequence[EyeExpectedValue]]:
    charts = repo.load_latest_charts(RaceSelector.select(race_id), analyser_name)
    if charts:
        return [EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2()]
    else:
        return None


@app.get("/analysis/{race_id}/{analyser_name}/{image_name}.png")
def get_image(race_id: str, analyser_name: str, image_name: str):
    charts = repo.load_latest_charts(RaceSelector.select(race_id), analyser_name)
    if charts:
        if image_name == "box":
            return Response(content=charts.model_box, media_type="image/png")
        elif image_name == "oc":
            return Response(content=charts.odds_chance, media_type="image/png")
        else:
            return Response(content="not found", status_code=404)

    else:
        return {"Status": "Not Analysed yet."}


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    start()
