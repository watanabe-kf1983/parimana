from collections import defaultdict
from typing import Mapping, Sequence

from pydantic import BaseModel

import parimana.domain.base as bs
import parimana.domain.analyse as an
import parimana.domain.race as rc


class Status(BaseModel):
    is_processing: bool
    has_analysis: bool
    is_odds_confirmed: bool


class OddsSourceInfo(BaseModel):
    source_uri: str
    odds_update_time: str

    @staticmethod
    def from_base(
        odds_source: rc.OddsSource,
        timestamp: rc.OddsTimeStamp,
    ):
        return OddsSourceInfo(
            source_uri=odds_source.get_uri(),
            odds_update_time=timestamp.long_str(),
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
        abilities: Mapping[bs.Contestant, an.Ability],
    ) -> Sequence["Competence"]:
        return sorted(
            (
                Competence.from_base(contestant=c, ability=a)
                for c, a in abilities.items()
            ),
            key=lambda c: c.mean,
        )


class CompetencesByPlace(BaseModel):
    place: str
    competences: Sequence[Competence]

    @staticmethod
    def from_base_mapping(
        abilities_by_place: Mapping[str, Mapping[bs.Contestant, an.Ability]],
    ) -> Sequence["CompetencesByPlace"]:

        return [
            CompetencesByPlace(
                place=place, competences=Competence.from_abilities(abilities)
            )
            for place, abilities in abilities_by_place.items()
        ]


class Correlations(BaseModel):
    a: str
    row: Mapping[str, float]


class Model(BaseModel):
    type: str
    competences: Sequence[Competence]
    competences_by_places: Sequence[CompetencesByPlace]
    competences_chart: str
    correlations: Sequence[Correlations]
    correlations_chart: str

    @staticmethod
    def from_base(
        charts: an.AnalysisCharts,
    ):
        model = charts.result.model
        crs = defaultdict(dict)
        for (a, b), v in model.correlations.items():
            crs[str(a)][str(b)] = v
        correlations = [Correlations(a=key, row=dict) for key, dict in crs.items()]

        return Model(
            type=model.name,
            competences=Competence.from_abilities(model.abilities),
            competences_by_places=CompetencesByPlace.from_base_mapping(
                model.abilities_by_place
            ),
            competences_chart=charts.model_box,
            correlations=correlations,
            correlations_chart=charts.model_mds,
        )


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


class Simulation(BaseModel):
    eev: Sequence[EyeExpectedValue]
    odds_chance_chart: str

    @staticmethod
    def from_base(
        charts: an.AnalysisCharts,
    ):
        return Simulation(
            eev=[EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2()],
            odds_chance_chart=charts.odds_chance,
        )


class Result(BaseModel):
    source: OddsSourceInfo
    model: Model
    simulation: Simulation

    @staticmethod
    def from_base(
        charts: an.AnalysisCharts,
        race: rc.Race,
        ost: rc.OddsTimeStamp,
    ):

        return Result(
            source=OddsSourceInfo.from_base(
                odds_source=race.odds_source, timestamp=ost
            ),
            model=Model.from_base(charts),
            simulation=Simulation.from_base(charts),
        )
