from typing import Any, AsyncGenerator, Mapping, Optional, Sequence
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import parimana.app.batch as batch
from parimana.app.analyse import AnalyseApp
from parimana.app.settings import Settings
from parimana.repository import FileRepository
import parimana.base as bs
import parimana.analyse as an
import parimana.race as rc


router = APIRouter()


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


app = AnalyseApp(FileRepository())


@router.post("/{race_id}/start")
def start_analyse(race_id: str):
    return {
        "task_id": batch.start_analyse(
            settings=Settings(race_id, analyser_names=["no_cor"])
        )
    }


@router.get("/{race_id}/status")
def get_status(race_id: str) -> Status:
    race = rc.Race.from_id(race_id)
    return Status(
        is_processing=app.is_processing(race),
        has_analysis=app.has_analysis(race),
        is_odds_confirmed=app.is_odds_confirmed(race),
    )


@router.get("/{race_id}/progress", response_class=StreamingResponse)
async def get_progress(race_id: str):
    race = rc.Race.from_id(race_id)
    return eventStreamResponse(app.get_progress(race))


@router.get("/{race_id}/{analyser_name}")
def get_analysis(race_id: str, analyser_name: str) -> Result:
    race = rc.Race.from_id(race_id)
    return Result.from_base(**app.get_analysis(race, analyser_name))


@router.get("/{race_id}/{analyser_name}/candidates")
def get_candidates(
    race_id: str, analyser_name: str, query: Optional[str] = Query(None)
) -> Sequence[EyeExpectedValue]:
    race = rc.Race.from_id(race_id)
    charts, _, __ = app.get_analysis(race, analyser_name)
    return [
        EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2(query=query)
    ]


def eventStreamResponse(generator: AsyncGenerator[str, Any]):
    return StreamingResponse(
        (f"data: {msg}\n\n" async for msg in generator), media_type="text/event-stream"
    )
