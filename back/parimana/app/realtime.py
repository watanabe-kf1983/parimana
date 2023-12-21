from pathlib import Path
from typing import Any, Sequence

from pydantic import BaseModel
from parimana.analyse.analysis_result import AnalysisCharts
from parimana.app.status import Status, StatusManager

import parimana.base
import parimana.analyse
from parimana.race import RaceSelector
from parimana.repository.file_repository import FileRepository
from parimana.app.settings import Settings
import parimana.app.batch as batch


class Eye(BaseModel):
    text: str
    type: str

    @staticmethod
    def from_base(eye: parimana.base.Eye):
        return Eye(text=eye.text, type=eye.type.name)


class EyeExpectedValue(BaseModel):
    eye: Eye
    odds: float
    chance: float
    expected: float

    @staticmethod
    def from_base(eev: parimana.analyse.EyeExpectedValue):
        return EyeExpectedValue(
            eye=Eye.from_base(eev.eye),
            odds=eev.odds,
            chance=eev.chance,
            expected=eev.expected,
        )


class Result(BaseModel):
    eev: Sequence[EyeExpectedValue]
    odds_chance: str
    model_box: str

    @staticmethod
    def from_base(charts: parimana.analyse.AnalysisCharts):
        return Result(
            eev=[EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2()],
            odds_chance=charts.odds_chance,
            model_box=charts.model_box,
        )


class ResultNotExistError(Exception):
    pass


repo = FileRepository(Path(".output"))


def start_wait_30() -> str:
    return batch.start_wait_30()


def get_wait_30_result(task_id: str) -> dict[str, Any]:
    return batch.get_wait_30_result(task_id)


# def start_analyse(settings: Settings):
#     task_id = batch.start_analyse(settings)
#     return {"task_id": task_id}


def start_analyse(race_id: str) -> str:
    settings = Settings(race_id, analyser_names=["no_cor"])
    return batch.start_analyse(settings)


def get_status(race_id: str) -> Status:
    race = RaceSelector.select(race_id)
    return StatusManager(race).load_status()


def get_analysis(race_id: str, analyser_name: str) -> Sequence[EyeExpectedValue]:
    charts = _get_charts(race_id, analyser_name)
    return Result.from_base(charts)


def _get_charts(race_id: str, analyser_name: str) -> AnalysisCharts:
    charts = repo.load_latest_charts(RaceSelector.select(race_id), analyser_name)
    if charts:
        return charts
    else:
        raise ResultNotExistError(f"{race_id}-{analyser_name} 's result not exists")
