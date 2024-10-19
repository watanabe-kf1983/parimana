import datetime
from typing import Mapping, Optional, Sequence
from fastapi import APIRouter, Query

import parimana.app.realtime_events as rt

router = APIRouter()


@router.get("/categories")
def get_categories():
    return rt.get_categories()


@router.get("/calendars")
def get_calendar(
    category_id: str = Query(min_length=1),
) -> Mapping[datetime.date, Sequence[rt.MeetingDay]]:
    return rt.get_calendar(rt.get_category(category_id))


@router.get("/races")
def get_races(
    category_id: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None),
    date: Optional[datetime.date] = Query(None),
    url: Optional[str] = Query(None),
) -> Sequence[rt.Race]:
    md = rt.MeetingDay(
        category=rt.get_category(category_id),
        course=rt.get_course(course_id),
        date=date,
    )
    return rt.get_races_by_meeting_day(md)


@router.get("/races/{race_id}")
def get_race(race_id: str) -> rt.Race:
    return rt.get_race(race_id)
