from typing import Optional, Sequence, Tuple

from parimana.domain.analyse import (
    analysers,
    AnalysisCharts,
    AnalysisResult,
)
from parimana.domain.analyse.expected import EyeExpectedValue, EyeExpectedValues
from parimana.domain.race import Race, OddsTimeStamp, RaceOddsPool
from parimana.io.kvs import Storage
from parimana.repository.analysis import AnalysisRepository, AnalysisRepositoryImpl
from parimana.app.exception import ResultNotExistError

_MODEL_LIST = ["no_cor", "ppf_mtx", "yurayura"]


class AnalyseApp:
    def __init__(self, store: Storage):
        self.repo: AnalysisRepository = AnalysisRepositoryImpl(store)

    def has_analysis(self, race: Race) -> bool:
        return self.repo.load_latest_charts_time(race) is not None

    def is_odds_confirmed(self, race: Race) -> bool:
        ct = self.repo.load_latest_charts_time(race)
        return (ct is not None) and ct.is_confirmed

    def list_latest_analysis(
        self, race: Race
    ) -> Tuple[Sequence[str], Optional[OddsTimeStamp]]:

        ts = self.repo.load_latest_charts_time(race)
        if ts:
            return self._list_analysis(race, ts), ts
        else:
            return [], None

    def _list_analysis(self, race: Race, ts: OddsTimeStamp) -> Sequence[str]:
        return [
            model
            for model in _MODEL_LIST
            if self.repo.charts_exists(race=race, ts=ts, model=model)
        ]

    def get_latest_analysis(
        self, race: Race, analyser_name: str
    ) -> Tuple[AnalysisCharts, OddsTimeStamp]:

        return self._get_latest_charts(race, analyser_name)

    def get_latest_time_stamp(self, race: Race) -> OddsTimeStamp:
        return self.repo.load_latest_charts_time(race)

    def get_candidates(
        self,
        race: Race,
        ts: OddsTimeStamp,
        analyser_name: str,
        query: Optional[str] = None,
    ) -> Sequence[EyeExpectedValue]:

        eevs = self._get_eevs(race, ts, analyser_name)
        return eevs.filter(query=query).values()

    # def get_combined_candidates(
    #     self, race: Race, ts: OddsTimeStamp, query: Optional[str] = None
    # ) -> Sequence[EyeExpectedValue]:

    #     eevs = EyeExpectedValues.combine(
    #         {
    #             name: self._get_eevs(race, ts, name)
    #             for name in self.list_latest_analysis(race)
    #         }
    #     )
    #     return eevs.filter(query=query).values()

    def _get_eevs(
        self, race: Race, ts: OddsTimeStamp, analyser_name: str
    ) -> EyeExpectedValues:
        charts = self.repo.load_charts(race, ts, analyser_name)
        if charts:
            return charts.result.eev
        else:
            raise ResultNotExistError(
                f"{race.race_id}-{analyser_name} 's result not exists"
            )

    def _get_latest_charts(
        self, race: Race, analyser_name: str
    ) -> Tuple[AnalysisCharts, OddsTimeStamp]:

        ts = self.repo.load_latest_charts_time(race)
        if ts:
            charts = self._get_charts(race, ts, analyser_name)
            return charts, ts

        else:
            raise ResultNotExistError(
                f"{race.race_id}-{analyser_name} 's result not exists"
            )

    def _get_charts(
        self, race: Race, ts: OddsTimeStamp, analyser_name: str
    ) -> AnalysisCharts:
        charts = self.repo.load_charts(race, ts, analyser_name)
        if charts:
            return charts
        else:
            raise ResultNotExistError(
                f"{race.race_id}-{analyser_name}-{ts} 's result not exists"
            )

    def analyse(
        self,
        odds_pool: RaceOddsPool,
        analyser_name: str,
        simulation_count: int,
    ) -> AnalysisResult:
        charts = self.repo.load_charts(
            odds_pool.race, odds_pool.timestamp, analyser_name
        )

        if charts:
            return charts.result
        else:
            r = analysers[analyser_name].analyse(odds_pool, simulation_count)
            self.repo.save_charts(odds_pool.race, odds_pool.timestamp, r.get_charts())
            return r
