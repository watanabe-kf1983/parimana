from typing import Optional, Sequence
from fastapi import APIRouter, Query

from parimana.ui.web.model.schedule import Category, RaceInfo
from parimana.context import context as cx

router = APIRouter()

app = cx.schedule_app
tasks = cx.schedule_tasks


@router.get("/categories")
def get_categories():
    return [Category.from_base(cat) for cat in app.category_selector.all()]


@router.get("/races")
def get_races(
    category_id: Optional[str] = Query(None),
    scraped_only: bool = Query(True),
    url: Optional[str] = Query(None),
) -> Sequence[RaceInfo]:
    if url:
        race = app.find_race(url)
        return [RaceInfo.from_base(race)] if race else []
    else:
        try:
            return [
                RaceInfo.from_base(race)
                for race in app.get_schedule(
                    cat=app.select_category(category_id), scraped_only=scraped_only
                )
            ]

        except Exception:
            return []


@router.get("/races/{race_id}")
def get_race(race_id: str) -> RaceInfo:
    return RaceInfo.from_base(app.get_race(race_id))


@router.post("/scrape/start")
def scrape_schedule():
    task_id = tasks.update_schedule_all().delay().id
    return {"task_id": task_id}


@router.post("/init-today/start")
def init_today():
    task_id = tasks.scrape_and_schedule_analyse.delay().id
    return {"task_id": task_id}
