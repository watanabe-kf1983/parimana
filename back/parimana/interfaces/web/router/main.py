from fastapi import APIRouter

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
