from fastapi import APIRouter, Query

from parimana.app.exception import ResultNotExistError
from parimana.interfaces.web.model.app import AppInfo
import parimana.interfaces.web.router.analyse as analyse
import parimana.interfaces.web.router.schedule as schedule
from parimana.context import context as cx

router = APIRouter()
router.include_router(analyse.router, prefix="/analyses", tags=["analysis"])
router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])


# health check
@router.get("/info")
def app_info() -> AppInfo:
    return AppInfo(status="ok", auto_analyse=cx.settings.auto_analyse_mode)


@router.get("/race_id")
def get_race_id(url: str = Query()) -> str:
    try:
        return cx.race_selector.select(url).race_id

    except ValueError:
        raise ResultNotExistError(f"URL {url} is not valid")
