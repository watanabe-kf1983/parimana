from typing import Sequence

from celery import group

from parimana.app.schedule import ScheduleApp
from parimana.domain.schedule import Category, RaceInfo
import parimana.settings as settings
from parimana.tasks.celery import app

schedule_app = ScheduleApp(
    categories=settings.categories, store=settings.schedule_storage
)


@app.task
def update_schedule(*, cat: Category) -> Sequence[RaceInfo]:
    return schedule_app.update_schedule(cat)


def update_schedule_all():
    return group(update_schedule.s(cat=cat) for cat in settings.categories)
