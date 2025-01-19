from typing import Optional, Sequence
from fastapi import APIRouter, Query

from parimana.interfaces.web.model.schedule import Category, RaceInfo
from parimana.context import context as cx

router = APIRouter()


@router.get("/categories")
def get_categories():
    return [Category.from_base(cat) for cat in cx.category_selector.all()]


@router.get("/races")
def get_races(
    category_id: Optional[str] = Query(None),
    analysed_only: bool = Query(True),
) -> Sequence[RaceInfo]:
    app = cx.schedule_app
    try:
        return [
            RaceInfo.from_base(race)
            for race in app.get_schedule(
                cat=app.select_category(category_id), analysed_only=analysed_only
            )
        ]

    except Exception:
        return []


@router.get("/races/{race_id}")
def get_race(race_id: str) -> RaceInfo:
    return RaceInfo.from_base(cx.schedule_app.get_race(race_id))


if not cx.settings.auto_analyse_mode:

    @router.post("/races/{race_id}")
    def start_analyse(race_id: str):
        cat = cx.category_selector.select_from_race_id(race_id)
        task_id = (
            cx.schedule_tasks.scrape_race_info.s(cat=cat, race_id=race_id).delay().id
        )
        return {"task_id": task_id}
