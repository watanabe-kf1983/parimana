from dataclasses import dataclass
from typing import Sequence

from celery import group

from parimana.app.schedule import ScheduleApp
from parimana.domain.schedule import Category, RaceInfo
from parimana.tasks.celery import task


@dataclass
class ScheduleTasks:
    schedule_app: ScheduleApp

    @task
    def update_schedule(self, *, cat: Category) -> Sequence[RaceInfo]:
        return self.schedule_app.update_schedule(cat)

    def update_schedule_all(self):
        return group(
            self.update_schedule.s(cat=cat)
            for cat in self.schedule_app.category_selector.all()
        )
