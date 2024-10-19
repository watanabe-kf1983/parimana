import datetime
from typing import Mapping, Optional, Sequence

from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str


categories = {
    "01": Category(id="01", name="ボートレース"),
    "02": Category(id="02", name="競馬(JRA)"),
}


class Course(BaseModel):
    id: str
    name: str


courses = {
    "01": Course(id="01", name="桐生"),
    "02": Course(id="02", name="府中"),
}


class MeetingDay(BaseModel):
    category: Category
    course: Course
    date: datetime.date


class Race(BaseModel):
    id: str
    name: str
    meeting_day: MeetingDay


def get_categories() -> Sequence[Category]:
    return [v for k, v in categories.items()]


def get_category(category_id: str) -> Optional[Category]:
    return categories.get(category_id, None)


def get_course(course_id: str) -> Optional[Course]:
    return courses.get(course_id, None)


def get_calendar(category: Category) -> Mapping[datetime.date, Sequence[MeetingDay]]:
    if category.id == "01":
        d = datetime.date.today()
        return {
            d: [
                MeetingDay(
                    category=category,
                    course=courses["01"],
                    date=d,
                )
            ]
        }
    else:
        return {}


def get_races_by_meeting_day(meeting_day: MeetingDay) -> Sequence[Race]:
    return [
        Race(
            id=f"boatrace-20240901-1-{i+1}",
            name=f"{i+1} R",
            meeting_day=meeting_day,
        )
        for i in range(12)
    ]


def find_race(url: str) -> Optional[Race]:
    return None


def get_race(race_id: str) -> Race:
    return Race(
        id=race_id,
        name=race_id,
        meeting_day=MeetingDay(
            category=categories["01"],
            course=courses["01"],
            date=datetime.date.today(),
        ),
    )
