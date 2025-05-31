from typing import Sequence
from fastapi import APIRouter, Query

from parimana.interfaces.web.model.schedule import RaceInfo
from parimana.context import context as cx

router = APIRouter()


@router.get("/races")
def get_races(
    analysed_only: bool = Query(True),
) -> Sequence[RaceInfo]:
    races = (
        cx.schedule_app.get_recent_analysed()
        if analysed_only
        else cx.schedule_app.get_recent_schedule()
    )
    return [RaceInfo.from_base(race) for race in races]


@router.get("/races/{race_id}")
def get_race(race_id: str) -> RaceInfo:
    return RaceInfo.from_base(cx.schedule_app.get_race(race_id))


if not cx.settings.auto_analyse_mode:

    @router.post("/races/{race_id}")
    def start_scrape_race_info(race_id: str):
        race = cx.race_selector.select(race_id)
        cat = cx.category_selector.select_from_race(race)
        task_id = (
            cx.schedule_tasks.scrape_race_info.s(cat=cat, race_id=race_id).delay().id
        )
        return {"task_id": task_id}
