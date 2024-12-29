from dataclasses import dataclass, field
from typing import Sequence

from celery import Celery, chain, group

from parimana.io.message import PublishCenter, mprint, mclose
from parimana.domain.analyse import AnalysisResult, default_analyser_names
from parimana.domain.race import Race, RaceOddsPool, RaceSelector
from parimana.app import AnalyseApp, OddsCollectorApp, ProcessStatusManager
from parimana.tasks.base import task, CeleryTasks


@dataclass(frozen=True)
class AnalyseTaskOptions:
    race_id: str
    use_cache: bool = False
    simulation_count: int = 10_000_000
    analyser_names: Sequence[str] = field(default_factory=default_analyser_names)
    recommend_query: str = ""
    recommend_size: int = 20


class AnalyseTasks(CeleryTasks):

    def __init__(
        self,
        analyse_app: AnalyseApp,
        odds_app: OddsCollectorApp,
        ps_manager: ProcessStatusManager,
        race_selector: RaceSelector,
        celery: Celery,
        publish_center: PublishCenter,
    ):
        super().__init__(celery=celery, publish_center=publish_center)
        self.analyse_app = analyse_app
        self.odds_app = odds_app
        self.ps_manager = ps_manager
        self.race_selector = race_selector

    @task
    def get_odds_pool(self, *, race: Race, scrape_force: bool = False) -> RaceOddsPool:
        return self.odds_app.get_odds_pool(race=race, scrape_force=scrape_force)

    @task
    def analyse(
        self, odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int
    ) -> AnalysisResult:
        return self.analyse_app.analyse(odds_pool, analyser_name, simulation_count)

    @task
    def start_process(self, *, process_name: str):
        self.ps_manager.start_process(process_name)

    @task
    def finish_process(self, results=None, /, *, process_name: str):
        self.ps_manager.finish_process(process_name)
        return results

    @task
    def handle_error(self, request, exc, traceback, *, process_name: str):
        mprint("ERROR occurred:")
        mprint(exc)
        mprint(traceback)
        mprint(f"Failed task info: args={request.args}, kwargs={request.kwargs}, ")
        mprint("")
        self.ps_manager.abort_process(process_name)
        mclose()

    def scrape_and_analyse(self, options: AnalyseTaskOptions):
        race = self.race_selector.select(options.race_id)
        process_name = f"analyse_{options.race_id}"
        return chain(
            self.start_process.s(channel_id=process_name, process_name=process_name),
            self.get_odds_pool.si(
                race=race, channel_id=process_name, scrape_force=not options.use_cache
            ),
            group(
                self.analyse.s(
                    analyser_name, options.simulation_count, channel_id=process_name
                )
                for analyser_name in options.analyser_names
            ),
            self.finish_process.s(channel_id=process_name, process_name=process_name),
        ).on_error(
            self.handle_error.s(channel_id=process_name, process_name=process_name)
        )
