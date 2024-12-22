from typing import Sequence, Tuple

from parimana.domain.analyse import (
    analysers,
    AnalysisCharts,
    EyeExpectedValue,
    AnalysisResult,
)
from parimana.domain.race import Race, OddsTimeStamp, RaceOddsPool
from parimana.io.kvs import Storage
from parimana.repository.analysis import AnalysisRepository, AnalysisRepositoryImpl
from parimana.app.exception import ResultNotExistError


class AnalyseApp:
    def __init__(self, store: Storage):
        self.repo: AnalysisRepository = AnalysisRepositoryImpl(store)

    def has_analysis(self, race: Race) -> bool:
        return self.repo.load_latest_charts_time(race) is not None

    def is_odds_confirmed(self, race: Race) -> bool:
        ct = self.repo.load_latest_charts_time(race)
        return (ct is not None) and ct.is_confirmed

    def get_analysis(
        self, race: Race, analyser_name: str
    ) -> Tuple[AnalysisCharts, Race, OddsTimeStamp]:
        return self._get_charts(race, analyser_name)

    def get_candidates(
        self, race: Race, analyser_name: str, query: str
    ) -> Sequence[EyeExpectedValue]:
        charts, _, __ = self._get_charts(race, analyser_name)
        return charts.result.recommend2(query=query)

    def _get_charts(
        self, race: Race, analyser_name: str
    ) -> Tuple[AnalysisCharts, Race, OddsTimeStamp]:
        if loaded := self.repo.load_latest_charts(race, analyser_name):
            charts, timestamp = loaded
            return charts, race, timestamp
        else:
            raise ResultNotExistError(
                f"{race.race_id}-{analyser_name} 's result not exists"
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
