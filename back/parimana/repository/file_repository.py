from dataclasses import dataclass
from pathlib import Path
import pickle


from parimana.analyse.analyse import AnalysisCharts


@dataclass(frozen=True)
class FileRepository:
    root_path: Path

    def save_charts(self, charts: AnalysisCharts):
        dir_ = self.root_path / charts.result.odds_pool.key / charts.result.model.name
        dir_.mkdir(exist_ok=True, parents=True)

        with open(dir_ / "charts.pickle", "wb") as f:
            pickle.dump(charts, f)

        with open(dir_ / "result.pickle", "wb") as f:
            pickle.dump(charts.result, f)

        with open(dir_ / f"{charts.result.model.name}.xlsx", "wb") as f:
            f.write(charts.excel)

        with open(dir_ / "oc.png", "wb") as f:
            f.write(charts.odds_chance)

        with open(dir_ / "box-plot.png", "wb") as f:
            f.write(charts.model_box)

        with open(dir_ / "mds.png", "wb") as f:
            f.write(charts.model_mds)

        with open(dir_ / "mds-metric.png", "wb") as f:
            f.write(charts.model_mds_metric)

    def save_odds_pool(self):
        pass
