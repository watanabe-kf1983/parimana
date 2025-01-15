from typing import Mapping, Sequence

from pydantic import BaseModel

import parimana.domain.base as bs
import parimana.domain.analyse as an
import parimana.domain.race as rc


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
    model_mds: str

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
            model_mds=charts.model_mds,
        )
