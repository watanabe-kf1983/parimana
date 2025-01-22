from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from parimana.domain.race import Race, OddsTimeStamp
from parimana.domain.analyse import AnalysisCharts
from parimana.io.kvs import Storage


class AnalysisRepository(ABC):

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
    def save_latest_charts_time(self, race: Race, ts: OddsTimeStamp) -> None:
        pass

    @abstractmethod
    def load_latest_charts_time(self, race: Race) -> Optional[OddsTimeStamp]:
        pass

    @abstractmethod
    def charts_exists_one(self, race: Race, model: str) -> bool:
        pass


@dataclass
class AnalysisRepositoryImpl(AnalysisRepository):
    store: Storage

    def save_charts(self, race: Race, timestamp: OddsTimeStamp, charts: AnalysisCharts):
        prefix = f"analysis/{race.race_id}/{timestamp}/{charts.result.model.name}"
        self.store.write_object(f"{prefix}/charts.pickle", charts)
        ts = self.load_latest_charts_time(race)
        if (ts is None) or (ts < timestamp):
            self.save_latest_charts_time(race, timestamp)

    def load_charts(self, race: Race, ts: OddsTimeStamp, model: str) -> AnalysisCharts:
        prefix = f"analysis/{race.race_id}/{ts}/{model}"
        return self.store.read_object(f"{prefix}/charts.pickle")

    def charts_exists(self, race: Race, ts: OddsTimeStamp, model: str) -> bool:
        prefix = f"analysis/{race.race_id}/{ts}/{model}"
        return self.store.exists(f"{prefix}/charts.pickle")

    def load_latest_charts(
        self, race: Race, model: str
    ) -> Optional[tuple[AnalysisCharts, OddsTimeStamp]]:
        ts = self.load_latest_charts_time(race)
        if ts:
            return self.load_charts(race, ts, model), ts
        else:
            return None

    def save_latest_charts_time(self, race: Race, ts: OddsTimeStamp) -> None:
        self.store.write_object(f"analysis/{race.race_id}/charts_ts.pickle", ts)

    def load_latest_charts_time(self, race: Race) -> Optional[OddsTimeStamp]:
        return self.store.read_object(f"analysis/{race.race_id}/charts_ts.pickle")

    def charts_exists_one(self, race: Race, model: str) -> bool:
        return self.store.exists(f"analysis/{race.race_id}/charts_ts.pickle")
