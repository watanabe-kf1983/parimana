from typing import Sequence

from parimana.app.schedule import ScheduleApp
from parimana.domain.schedule import Category, RaceInfo
import parimana.settings as settings
from parimana.tasks.celery import app

schedule_app = ScheduleApp(
    categories=settings.categories, store=settings.schedule_storage
)


@app.task
def get_schedule(*, cat: Category) -> Sequence[RaceInfo]:
    return schedule_app.scrape_and_get_schedule(cat)
