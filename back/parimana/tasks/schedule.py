from typing import Sequence

from celery import Celery, group

from parimana.io.message import PublishCenter
from parimana.app import ScheduleApp
from parimana.domain.schedule import Category, RaceInfo
from parimana.tasks.base import CeleryTasks, task


class ScheduleTasks(CeleryTasks):
    def __init__(
        self,
        schedule_app: ScheduleApp,
        celery: Celery,
        publish_center: PublishCenter,
    ):
        super().__init__(celery=celery, publish_center=publish_center)
        self.schedule_app = schedule_app

    @task
    def update_schedule(self, *, cat: Category) -> Sequence[RaceInfo]:
        return self.schedule_app.update_schedule(cat)

    def update_schedule_all(self):
        return group(
            self.update_schedule.s(cat=cat)
            for cat in self.schedule_app.category_selector.all()
        )
