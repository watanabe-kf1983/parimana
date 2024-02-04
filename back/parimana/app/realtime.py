from typing import Any, Sequence, Tuple

from pydantic import BaseModel

import parimana.base as bs
import parimana.analyse as an
import parimana.race as rc
from parimana.app.status import ProcessStatusManager
from parimana.app.settings import Settings
from parimana.repository.file_repository import FileRepository
import parimana.app.batch as batch


class Eye(BaseModel):
    text: str
    type: str

    @staticmethod
    def from_base(eye: bs.Eye):
        return Eye(text=eye.text, type=eye.type.name)


class EyeExpectedValue(BaseModel):
    eye: Eye
    odds: float
    chance: float
    expected: float

    @staticmethod
    def from_base(eev: an.EyeExpectedValue):
        return EyeExpectedValue(
            eye=Eye.from_base(eev.eye),
            odds=eev.odds,
            chance=eev.chance,
            expected=eev.expected,
        )


class Status(BaseModel):
    is_processing: bool
    has_analysis: bool
    is_odds_confirmed: bool


class Result(BaseModel):
    eev: Sequence[EyeExpectedValue]
    source_uri: str
    odds_update_time: str
    odds_chance: str
    model_box: str

    @staticmethod
    def from_base(
        charts: an.AnalysisCharts,
        race: rc.Race,
        ost: rc.OddsTimeStamp,
    ):
        return Result(
            eev=[EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2()],
            source_uri=race.source.get_uri(),
            odds_update_time=ost.long_str(),
            odds_chance=charts.odds_chance,
            model_box=charts.model_box,
        )


class ResultNotExistError(Exception):
    pass


repo = FileRepository()


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
    race = rc.RaceSelector.select(race_id)
    is_processing = ProcessStatusManager(race).load_status().is_processing
    ct = repo.load_latest_charts_time(race)
    has_analysis = ct is not None
    is_odds_confirmed = has_analysis and ct.is_confirmed
    return Status(
        is_processing=is_processing,
        has_analysis=has_analysis,
        is_odds_confirmed=is_odds_confirmed,
    )


def get_analysis(race_id: str, analyser_name: str) -> Sequence[EyeExpectedValue]:
    return Result.from_base(*_get_charts(race_id, analyser_name))


def _get_charts(
    race_id: str, analyser_name: str
) -> Tuple[an.AnalysisCharts, rc.Race, rc.OddsTimeStamp]:
    race = rc.RaceSelector.select(race_id)
    if loaded := repo.load_latest_charts(race, analyser_name):
        charts, timestamp = loaded
        return charts, race, timestamp
    else:
        raise ResultNotExistError(f"{race_id}-{analyser_name} 's result not exists")
