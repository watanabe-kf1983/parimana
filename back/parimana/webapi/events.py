import datetime
from typing import Mapping, Optional, Sequence
from fastapi import APIRouter, Query

import parimana.app.realtime_events as rt

router = APIRouter()


@router.get("/categories")
def get_categories():
    return rt.get_categories()


@router.get("/calendars/{category_id}")
def get_calendar(category_id: str) -> Mapping[datetime.date, Sequence[rt.Course]]:
    return rt.get_calendar(rt.get_category(category_id))


@router.get("/races")
def get_races(
    course_id: Optional[str] = Query(None),
    date: Optional[datetime.date] = Query(None),
    url: Optional[str] = Query(None),
) -> Sequence[rt.Race]:
    if url:
        race = rt.find_race(url)
        return [race] if race else []
    else:
        try:
            return rt.get_races_by_course(course=rt.get_course(course_id), date=date)

        except Exception:
            return []


@router.get("/races/{race_id}")
def get_race(race_id: str) -> rt.Race:
    return rt.get_race(race_id)
