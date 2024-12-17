from typing import Optional, Sequence
from fastapi import APIRouter, Query

import parimana.app.realtime_schedule as rt

router = APIRouter()


@router.get("/categories")
def get_categories():
    return rt.get_categories()


@router.get("/races/")
def get_races(
    category_id: Optional[str] = Query(None),
    url: Optional[str] = Query(None),
) -> Sequence[rt.RaceInfo]:
    if url:
        race = rt.find_race(url)
        return [race] if race else []
    else:
        try:
            return rt.get_schedule(cat=rt.get_category(category_id))

        except Exception:
            return []


@router.get("/races/{race_id}")
def get_race(race_id: str) -> rt.RaceInfo:
    return rt.get_race(race_id)
