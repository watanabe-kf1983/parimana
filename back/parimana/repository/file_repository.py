from dataclasses import dataclass
from pathlib import Path
import pickle
from typing import Optional


from parimana.race.race import Race
from parimana.race.odds_pool import OddsTimeStamp, RaceOddsPool
from parimana.analyse import AnalysisCharts


@dataclass(frozen=True)
class FileRepository:
    root_path: Path

    def save_odds_pool(self, odds_pool: RaceOddsPool):
        write_as_pickle(
            self._op_dir(odds_pool.race, odds_pool.timestamp) / "odds_pool.pickle",
            odds_pool,
        )
        ts = self.load_latest_odds_time(odds_pool.race)
        if (ts is None) or (ts < odds_pool.timestamp):
            self.save_latest_odds_time(odds_pool.race, odds_pool.timestamp)

    def load_odds_pool(self, race: Race, ts: OddsTimeStamp) -> Optional[RaceOddsPool]:
        return read_pickle(
            self._op_dir(race, ts) / "odds_pool.pickle",
        )

    def load_latest_odds_pool(self, race: Race) -> Optional[RaceOddsPool]:
        ts = self.load_latest_odds_time(race)
        if ts:
            return self.load_odds_pool(race, ts)
        else:
            return None

    def odds_pool_exists(self, race: Race) -> bool:
        return (self._race_dir(race) / "odds_ts.pickle").exists()

    def save_charts(self, race: Race, timestamp: OddsTimeStamp, charts: AnalysisCharts):
        dir_ = self._result_dir(race, timestamp, charts.result.model.name)
        write_as_pickle(dir_ / "charts.pickle", charts)
        write_as_pickle(dir_ / "result.pickle", charts.result)
        write_bytes(dir_ / "result.xlsx", charts.excel)
        write_bytes(dir_ / "oc.png", charts.odds_chance)
        write_bytes(dir_ / "box-plot.png", charts.model_box)
        write_bytes(dir_ / "mds.png", charts.model_mds)
        write_bytes(dir_ / "mds-metric.png", charts.model_mds_metric)

        ts = self.load_latest_charts_time(race)
        if (ts is None) or (ts < timestamp):
            self.save_latest_charts_time(race, timestamp)

    def load_charts(self, race: Race, ts: OddsTimeStamp, model: str) -> AnalysisCharts:
        dir_ = self._result_dir(race, ts, model)
        return read_pickle(dir_ / "charts.pickle")

    def load_latest_charts(self, race: Race, model: str) -> Optional[AnalysisCharts]:
        ts = self.load_latest_charts_time(race)
        if ts:
            return self.load_charts(race, ts, model)
        else:
            return None

    def _race_dir(self, race: Race) -> Path:
        dir_ = self.root_path / race.race_id
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_

    def _op_dir(self, race: Race, ts: OddsTimeStamp) -> Path:
        dir_ = self._race_dir(race) / str(ts)
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_

    def _result_dir(self, race: Race, ts: OddsTimeStamp, model: str) -> Path:
        dir_ = self._op_dir(race, ts) / model
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_

    def save_latest_odds_time(self, race: Race, ts: OddsTimeStamp) -> None:
        write_as_pickle(self._race_dir(race) / "odds_ts.pickle", ts)

    def load_latest_odds_time(self, race: Race) -> Optional[OddsTimeStamp]:
        return read_pickle(self._race_dir(race) / "odds_ts.pickle")

    def save_latest_charts_time(self, race: Race, ts: OddsTimeStamp) -> None:
        write_as_pickle(self._race_dir(race) / "charts_ts.pickle", ts)

    def load_latest_charts_time(self, race: Race) -> Optional[OddsTimeStamp]:
        return read_pickle(self._race_dir(race) / "charts_ts.pickle")


def read_pickle(file_path: Path):
    if file_path.exists():
        print(f"reading {file_path}...")
        with open(file_path, "rb") as f:
            return pickle.load(f)
    else:
        return None


def write_as_pickle(file_path: Path, obj):
    with open(file_path, "wb") as f:
        print(f"writing {file_path}...")
        pickle.dump(obj, f)


def write_bytes(file_path: Path, binary: bytes):
    with open(file_path, "wb") as f:
        print(f"writing {file_path}...")
        f.write(binary)
