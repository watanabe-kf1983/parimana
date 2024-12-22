from dataclasses import dataclass, field
from typing import Sequence
from celery import chain, group

from parimana.io.message import mprint, mclose
from parimana.domain.analyse import AnalysisResult, default_analyser_names
from parimana.domain.race import Race, RaceOddsPool, RaceSelector
from parimana.app.analyse import AnalyseApp
from parimana.app.collect_odds import OddsCollectorApp
from parimana.app.status import ProcessStatusManager
from parimana.tasks.celery import app
import parimana.settings as settings

analyse_app = AnalyseApp(store=settings.analysis_storage)
odds_app = OddsCollectorApp(store=settings.odds_storage)
ps_manager = ProcessStatusManager(
    store=settings.status_storage, center=settings.publish_center
)
race_selector = RaceSelector(settings.race_types)

with_channel_printer = settings.publish_center.with_channel_printer


@app.task
@with_channel_printer
def get_odds_pool(*, race: Race, scrape_force: bool = False) -> RaceOddsPool:
    return odds_app.get_odds_pool(race=race, scrape_force=scrape_force)


@app.task
@with_channel_printer
def analyse(
    odds_pool: RaceOddsPool, analyser_name: str, simulation_count: int
) -> AnalysisResult:
    return analyse_app.analyse(odds_pool, analyser_name, simulation_count)


@app.task
@with_channel_printer
def start_process(*, process_name: str):
    ps_manager.start_process(process_name)


@app.task
@with_channel_printer
def finish_process(results=None, /, *, process_name: str):
    ps_manager.finish_process(process_name)
    return results


@app.task
@with_channel_printer
def handle_error(request, exc, traceback, *, process_name: str):
    mprint("ERROR occurred:")
    mprint(exc)
    mprint(traceback)
    mprint(f"Failed task info: args={request.args}, kwargs={request.kwargs}, ")
    mprint("")
    ps_manager.abort_process(process_name)
    mclose()


@dataclass(frozen=True)
class AnalyseTaskOptions:
    race_id: str
    use_cache: bool = False
    simulation_count: int = 10_000_000
    analyser_names: Sequence[str] = field(default_factory=default_analyser_names)
    recommend_query: str = ""
    recommend_size: int = 20


def scrape_and_analyse(options: AnalyseTaskOptions):
    race = race_selector.select(options.race_id)
    process_name = f"analyse_{options.race_id}"
    return chain(
        start_process.s(channel_id=process_name, process_name=process_name),
        get_odds_pool.si(
            race=race, channel_id=process_name, scrape_force=not options.use_cache
        ),
        group(
            analyse.s(analyser_name, options.simulation_count, channel_id=process_name)
            for analyser_name in options.analyser_names
        ),
        finish_process.s(channel_id=process_name, process_name=process_name),
    ).on_error(handle_error.s(channel_id=process_name, process_name=process_name))
