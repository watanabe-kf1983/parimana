from typing import Callable, Collection, Sequence
import datetime
from datetime import timedelta

from celery import Celery, Task, chain, group

from parimana.io.kvs import Storage
from parimana.io.message import mprint
from parimana.app import ScheduleApp
from parimana.domain.schedule import Category, RaceInfo
from parimana.tasks.base import CeleryTasks, task
from parimana.tasks.analyse import AnalyseTaskOptions


class ScheduleTasks(CeleryTasks):
    def __init__(
        self,
        schedule_app: ScheduleApp,
        analyse_task_provider: Callable[[AnalyseTaskOptions], Task],
        task_schedule_kvs: Storage,
        celery: Celery,
    ):
        super().__init__(celery=celery)
        self.schedule_app = schedule_app
        self.analyse_task_provider = analyse_task_provider
        self.task_schedule_kvs = task_schedule_kvs
        self.prepare_task()

    @task
    def update_schedule(self, *, cat: Category, **kwargs) -> Sequence[RaceInfo]:
        return self.schedule_app.update_schedule(cat)

    @task
    def schedule_analyse(self, min: int = 30, **kwargs) -> None:
        for race in self.schedule_app.get_today_schedule():
            now = datetime.datetime.now(tz=race.fixture.course.category.timezone)
            analyse_schedule = race.generate_analyse_schedule(
                closing_time_delta_list=[5, -7, -20, -60, -180],
                time_fron=now,
                time_to=now + timedelta(minutes=min),
            )
            for eta in analyse_schedule:
                task_key = f"task/analyse/{race.race_id}/{int(eta.timestamp())}"
                if not self.task_schedule_kvs.exists(task_key):
                    self.task_schedule_kvs.write_binary(task_key, b"scheduled")

                    options = AnalyseTaskOptions(
                        race.race_id, analyser_names=["no_cor"]
                    )
                    self.analyse_task_provider(options=options).apply_async(
                        eta=eta, expires=(eta + timedelta(minutes=10))
                    )
                    mprint(f"Analyse of {race.race_id} at {eta} scheduled.")
                else:
                    mprint(f"Analyse of {race.race_id} at {eta} skipped.")

    @task
    def handle_error(self, request, exc, traceback, **kwargs):
        mprint("ERROR occurred:")
        mprint(exc)
        mprint(traceback)
        mprint(f"Failed task info: args={request.args}, kwargs={request.kwargs}, ")
        mprint("")

    def scrape_and_schedule_analyse(self, min: int = 30):
        return chain(
            self.update_schedule_all(),
            self.schedule_analyse.si(min=min),
        ).on_error(self.handle_error.s())

    def update_schedule_all(self):
        return group(
            self.update_schedule.si(cat=cat)
            for cat in self.schedule_app.category_selector.all()
        )

    def queue_broker(self, *args, **kwargs) -> str:
        if cat := kwargs.get("cat"):
            if isinstance(cat, Category):
                return f"scrape_{cat.schedule_source.site_name()}"

        return super().queue_broker(*args, **kwargs)

    def queues(self) -> Collection[str]:
        sites = self.schedule_app.category_selector.source_sites()
        return [f"scrape_{site}" for site in sites] + ["default"]
