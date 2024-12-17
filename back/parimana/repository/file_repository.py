import datetime
import os
from dataclasses import dataclass, field
from pathlib import Path
import pickle
from typing import Optional, Sequence

import plotly.io as pio

from parimana.message import mprint
from parimana.race.base import Race, OddsTimeStamp, RaceOddsPool
from parimana.race.schedule import Category, RaceInfo
from parimana.analyse import AnalysisCharts


def repository_path() -> Path:
    return Path(os.getenv("FILE_REPO_PATH", ".output"))


@dataclass(frozen=True)
class FileRepository:
    root_path: Path = field(default_factory=repository_path)

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
        write_bytes(dir_ / "result.xlsx", charts.excel)
        write_html_chart(dir_ / "oc.html", charts.odds_chance)
        write_html_chart(dir_ / "box-plot.html", charts.model_box)
        # write_html_chart(dir_ / "mds.html", charts.model_mds)
        # write_html_chart(dir_ / "mds-metric.html", charts.model_mds_metric)

        ts = self.load_latest_charts_time(race)
        if (ts is None) or (ts < timestamp):
            self.save_latest_charts_time(race, timestamp)

    def load_charts(self, race: Race, ts: OddsTimeStamp, model: str) -> AnalysisCharts:
        dir_ = self._result_dir(race, ts, model)
        return read_pickle(dir_ / "charts.pickle")

    def load_latest_charts(
        self, race: Race, model: str
    ) -> Optional[tuple[AnalysisCharts, OddsTimeStamp]]:
        ts = self.load_latest_charts_time(race)
        if ts:
            return self.load_charts(race, ts, model), ts
        else:
            return None

    def save_calendar(
        self,
        cat: Category,
        calendar: Sequence[datetime.date],
    ):
        dir_ = self._cat_dir(cat)
        write_as_pickle(
            dir_
            / f"calendar{datetime.datetime.now(cat.timezone).date():%Y%m%d}.pickle",
            calendar,
        )

    def load_calendar(self, cat: Category) -> Optional[Sequence[datetime.date]]:
        dir_ = self._cat_dir(cat)
        return read_pickle(
            dir_ / f"calendar{datetime.datetime.now(cat.timezone).date():%Y%m%d}.pickle"
        )

    def save_schedule(
        self,
        cat: Category,
        date: datetime.date,
        schedule: Sequence[RaceInfo],
    ):
        dir_ = self._cat_dir(cat)
        write_as_pickle(dir_ / f"{date:%Y%m%d}_schedule.pickle", schedule)

    def load_schedule(
        self, cat: Category, date: datetime.date
    ) -> Optional[Sequence[RaceInfo]]:
        dir_ = self._cat_dir(cat)
        return read_pickle(dir_ / f"{date:%Y%m%d}_schedule.pickle")

    def save_race_info(self, race_info: RaceInfo):
        write_as_pickle(
            self._schedule_race_dir() / f"{race_info.race_id}.pickle",
            race_info,
        )

    def load_race_info(self, race_id: str) -> Optional[RaceInfo]:
        return read_pickle(
            self._schedule_race_dir() / f"{race_id}.pickle",
        )

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

    def _cat_dir(self, cat: Category) -> Path:
        dir_ = self.root_path / "schedule" / "cat" / cat.id
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_

    def _schedule_race_dir(self) -> Path:
        dir_ = self.root_path / "schedule" / "races"
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

    def save_process_status(self, race: Race, status: str) -> None:
        write_text(self._race_dir(race) / "status.txt", status)

    def load_process_status(self, race: Race) -> Optional[str]:
        return read_text(self._race_dir(race) / "status.txt")


def read_text(file_path: Path) -> Optional[str]:
    if file_path.exists():
        with open(file_path, "r") as f:
            return f.read()
    else:
        return None


def write_text(file_path: Path, txt: str) -> None:
    with open(file_path, "w") as f:
        f.write(txt)


def write_html_chart(file_path: Path, chart_json: str) -> None:
    chart = pio.from_json(chart_json)
    html = chart.to_html(include_plotlyjs="cdn", include_mathjax="cdn")
    write_text(file_path, html)


def read_pickle(file_path: Path):
    if file_path.exists():
        mprint(f"reading {file_path}...")
        with open(file_path, "rb") as f:
            return pickle.load(f)
    else:
        return None


def write_as_pickle(file_path: Path, obj):
    with open(file_path, "wb") as f:
        mprint(f"writing {file_path}...")
        pickle.dump(obj, f)


def write_bytes(file_path: Path, binary: bytes):
    with open(file_path, "wb") as f:
        mprint(f"writing {file_path}...")
        f.write(binary)
