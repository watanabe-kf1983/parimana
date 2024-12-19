from abc import ABC, abstractmethod
from typing import Optional, Sequence, Tuple


from parimana.domain.analyse import (
    analysers,
    AnalysisCharts,
    EyeExpectedValue,
    AnalysisResult,
)
from parimana.domain.race import Race, OddsTimeStamp, RaceOddsPool
from parimana.app.exception import ResultNotExistError


class AnalysisRepository(ABC):

    @abstractmethod
    def save_odds_pool(self, odds_pool: RaceOddsPool):
        pass

    @abstractmethod
    def load_odds_pool(self, race: Race, ts: OddsTimeStamp) -> Optional[RaceOddsPool]:
        pass

    @abstractmethod
    def load_latest_odds_pool(self, race: Race) -> Optional[RaceOddsPool]:
        pass

    @abstractmethod
    def odds_pool_exists(self, race: Race) -> bool:
        pass

    @abstractmethod
    def save_charts(self, race: Race, timestamp: OddsTimeStamp, charts: AnalysisCharts):
        pass

    @abstractmethod
    def load_charts(self, race: Race, ts: OddsTimeStamp, model: str) -> AnalysisCharts:
        pass

    @abstractmethod
    def load_latest_charts(
        self, race: Race, model: str
    ) -> Optional[tuple[AnalysisCharts, OddsTimeStamp]]:
        pass

    @abstractmethod
    def save_latest_odds_time(self, race: Race, ts: OddsTimeStamp) -> None:
        pass

    @abstractmethod
    def load_latest_odds_time(self, race: Race) -> Optional[OddsTimeStamp]:
        pass

    @abstractmethod
    def save_latest_charts_time(self, race: Race, ts: OddsTimeStamp) -> None:
        pass

    @abstractmethod
    def load_latest_charts_time(self, race: Race) -> Optional[OddsTimeStamp]:
        pass


class AnalyseApp:
    def __init__(self, repo: AnalysisRepository):
        self.repo: AnalysisRepository = repo

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

    def get_odds_pool(self, *, race: Race, scrape_force: bool = False) -> RaceOddsPool:
        odds_pool = self.repo.load_latest_odds_pool(race)

        if odds_pool and (odds_pool.timestamp.is_confirmed or not scrape_force):
            return odds_pool
        else:
            timestamp = race.odds_source.scrape_timestamp()
            if (not odds_pool) or odds_pool.timestamp < timestamp:
                odds_pool = race.odds_source.scrape_odds_pool()
                self.repo.save_odds_pool(odds_pool)
            return odds_pool

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
