from typing import Any, AsyncGenerator, Mapping, Sequence, Tuple

from pydantic import BaseModel

import parimana.base as bs
import parimana.analyse as an
import parimana.race as rc
import parimana.message as mg
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


Q1_STD_NORMAL = -0.674489750196082


class Competence(BaseModel):
    contestant: str
    mean: float
    q1: float
    q3: float
    sd: float

    @staticmethod
    def from_base(contestant: bs.Contestant, ability: an.Ability) -> "Competence":
        mean = ability.expected_value
        sd = ability.uncertainty
        return Competence(
            contestant=contestant.name,
            mean=mean,
            q1=mean + sd * Q1_STD_NORMAL,
            q3=mean - sd * Q1_STD_NORMAL,
            sd=sd,
        )

    @staticmethod
    def from_abilities(
        abilities: Mapping[bs.Contestant, an.Ability]
    ) -> Sequence["Competence"]:
        return sorted(
            (
                Competence.from_base(contestant=c, ability=a)
                for c, a in abilities.items()
            ),
            key=lambda c: c.mean,
        )


class Status(BaseModel):
    is_processing: bool
    has_analysis: bool
    is_odds_confirmed: bool


class Result(BaseModel):
    eev: Sequence[EyeExpectedValue]
    competences: Sequence[Competence]
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
            competences=Competence.from_abilities(charts.result.model.abilities),
            source_uri=race.odds_source.get_uri(),
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


def start_analyse(race_id: str) -> str:
    settings = Settings(race_id, analyser_names=["no_cor"])
    return batch.start_analyse(settings)


def get_status(race_id: str) -> Status:
    race = rc.RaceSelector.select(race_id)
    is_processing = ProcessStatusManager(repo, race).load_status().is_processing
    ct = repo.load_latest_charts_time(race)
    has_analysis = ct is not None
    is_odds_confirmed = has_analysis and ct.is_confirmed
    return Status(
        is_processing=is_processing,
        has_analysis=has_analysis,
        is_odds_confirmed=is_odds_confirmed,
    )


def get_analysis(race_id: str, analyser_name: str) -> Result:
    return Result.from_base(*_get_charts(race_id, analyser_name))


def get_candidates(
    race_id: str, analyser_name: str, query: str
) -> Sequence[EyeExpectedValue]:
    charts, _, __ = _get_charts(race_id, analyser_name)
    return [
        EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2(query=query)
    ]


def get_progress(race_id: str) -> AsyncGenerator[str, Any]:
    return mg.Channel(race_id).alisten()


def _get_charts(
    race_id: str, analyser_name: str
) -> Tuple[an.AnalysisCharts, rc.Race, rc.OddsTimeStamp]:
    race = rc.RaceSelector.select(race_id)
    if loaded := repo.load_latest_charts(race, analyser_name):
        charts, timestamp = loaded
        return charts, race, timestamp
    else:
        raise ResultNotExistError(f"{race_id}-{analyser_name} 's result not exists")
