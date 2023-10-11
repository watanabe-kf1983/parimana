from pathlib import Path
from typing import Any, Optional, Sequence

from pydantic import BaseModel

import parimana.base
import parimana.analyse
from parimana.race import RaceSelector
from parimana.repository.file_repository import FileRepository
from parimana.app.settings import Settings
import parimana.app.batch as batch


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


repo = FileRepository(Path(".output"))


def start_wait_30() -> str:
    return batch.start_wait_30()


def get_wait_30_result(task_id: str) -> dict[str, Any]:
    return batch.get_wait_30_result(task_id)


# def start_analyse(settings: Settings):
#     task_id = batch.start_analyse(settings)
#     return {"task_id": task_id}


def start_analyse(race_id: str) -> str:
    settings = Settings(race_id, analyser_names=["no_cor", "ppf_mtx"])
    return batch.start_analyse(settings)


def get_analysis(
    race_id: str, analyser_name: str
) -> Optional[Sequence[EyeExpectedValue]]:
    charts = repo.load_latest_charts(RaceSelector.select(race_id), analyser_name)
    if charts:
        return [EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2()]
    else:
        return None


def get_box_image(race_id: str, analyser_name: str):
    charts = repo.load_latest_charts(RaceSelector.select(race_id), analyser_name)
    if charts:
        return charts.model_box
    else:
        return None


def get_oc_image(race_id: str, analyser_name: str):
    charts = repo.load_latest_charts(RaceSelector.select(race_id), analyser_name)
    if charts:
        return charts.odds_chance
    else:
        return None
