from typing import Optional, Sequence
from fastapi import APIRouter, Query

from parimana.ui.web.model.schedule import Category, RaceInfo
from parimana.context import context as cx

router = APIRouter()


@router.get("/categories")
def get_categories():
    return [Category.from_base(cat) for cat in cx.category_selector.all()]


@router.get("/races")
def get_races(
    category_id: Optional[str] = Query(None),
    analysed_only: bool = Query(True),
    url: Optional[str] = Query(None),
) -> Sequence[RaceInfo]:
    app = cx.schedule_app
    if url:
        race = app.find_race(url)
        return [RaceInfo.from_base(race)] if race else []
    else:
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
