from typing import Any, AsyncGenerator, Mapping, Optional, Sequence
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from parimana.app.collect_odds import OddsCollectorApp
import parimana.domain.base as bs
import parimana.domain.analyse as an
import parimana.domain.race as rc
from parimana.app.status import ProcessStatusManager
from parimana.app.analyse import AnalyseApp
from parimana.tasks import AnalyseTasks, AnalyseTaskOptions
import parimana.settings as settings


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


pub_center = settings.publish_center
app = AnalyseApp(store=settings.analysis_storage)
psm = ProcessStatusManager(store=settings.status_storage, center=pub_center)
race_selector = rc.RaceSelector(settings.race_types)
odds_app = OddsCollectorApp(store=settings.odds_storage)

tasks = AnalyseTasks(
    analyse_app=app,
    odds_app=odds_app,
    ps_manager=psm,
    race_selector=race_selector,
)

router = APIRouter()


@router.post("/{race_id}/start")
def start_analyse(race_id: str):
    options = AnalyseTaskOptions(race_id, analyser_names=["no_cor"])
    task_id = tasks.scrape_and_analyse(options).delay().id
    return {"task_id": task_id}


@router.get("/{race_id}/status")
def get_status(race_id: str) -> Status:
    race = race_selector.select(race_id)
    return Status(
        is_processing=psm.load_status(f"analyse_{race_id}").is_processing,
        has_analysis=app.has_analysis(race),
        is_odds_confirmed=app.is_odds_confirmed(race),
    )


@router.get("/{race_id}/progress", response_class=StreamingResponse)
async def get_progress(race_id: str):
    return _eventStreamResponse(pub_center.get_channel(f"analyse_{race_id}").alisten())


@router.get("/{race_id}/{analyser_name}")
def get_analysis(race_id: str, analyser_name: str) -> Result:
    race = race_selector.select(race_id)
    return Result.from_base(*app.get_analysis(race, analyser_name))


@router.get("/{race_id}/{analyser_name}/candidates")
def get_candidates(
    race_id: str, analyser_name: str, query: Optional[str] = Query(None)
) -> Sequence[EyeExpectedValue]:
    race = race_selector.select(race_id)
    charts, _, __ = app.get_analysis(race, analyser_name)
    return [
        EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2(query=query)
    ]


def _eventStreamResponse(generator: AsyncGenerator[str, Any]):
    return StreamingResponse(
        (f"data: {msg}\n\n" async for msg in generator), media_type="text/event-stream"
    )
