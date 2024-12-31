from typing import Callable, Collection, Sequence
import datetime
from datetime import timedelta

from celery import Celery, Task, chain, group

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
        celery: Celery,
    ):
        super().__init__(celery=celery)
        self.schedule_app = schedule_app
        self.analyse_task_provider = analyse_task_provider
        self.prepare_task()

    @task
    def update_schedule(self, *, cat: Category, **kwargs) -> Sequence[RaceInfo]:
        return self.schedule_app.update_schedule(cat)

    @task
    def schedule_analyse(self, **kwargs) -> None:
        for race in self.schedule_app.get_today_schedule():
            now = datetime.datetime.now(tz=race.fixture.course.category.timezone)
            mprint(race)
            mprint(now)
            mprint(race.poll_start_time)
            mprint(race.poll_closing_time + timedelta(minutes=5))
            mprint(race.poll_closing_time + timedelta(minutes=-7))
            mprint(race.poll_closing_time + timedelta(minutes=-20))
            mprint(race.poll_closing_time + timedelta(minutes=-60))
            mprint(race.poll_closing_time + timedelta(minutes=-180))
            analyse_schedule = set(
                max(
                    now,
                    race.poll_start_time,
                    (race.poll_closing_time + timedelta(minutes=delta_min)),
                )
                for delta_min in [5, -7, -20, -60, -180]
            )
            mprint(analyse_schedule)
            for eta in analyse_schedule:
                options = AnalyseTaskOptions(race.race_id, analyser_names=["no_cor"])
                self.analyse_task_provider(options=options).apply_async(eta=eta)
                mprint(f"Analyse of {race.race_id} scheduled at {eta}")

    def start_periodic_analyse(self):
        return chain(
            self.update_schedule_all(),
            self.schedule_analyse.si(),
        )

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
