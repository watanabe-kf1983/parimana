from typing import Collection, Sequence

from celery import Celery, group

from parimana.app import ScheduleApp
from parimana.domain.schedule import Category, RaceInfo
from parimana.tasks.base import CeleryTasks, task


class ScheduleTasks(CeleryTasks):
    def __init__(self, schedule_app: ScheduleApp, celery: Celery):
        super().__init__(celery=celery)
        self.schedule_app = schedule_app
        self.prepare_task()

    @task
    def update_schedule(self, *, cat: Category, **kwargs) -> Sequence[RaceInfo]:
        return self.schedule_app.update_schedule(cat)

    def update_schedule_all(self):
        return group(
            self.update_schedule.s(
                cat=cat, queue=f"scrape_{cat.schedule_source.site_name()}"
            )
            for cat in self.schedule_app.category_selector.all()
        )

    def queues(self) -> Collection[str]:
        sites = self.schedule_app.category_selector.source_sites()
        return [f"scrape_{site}" for site in sites] + ["default"]
