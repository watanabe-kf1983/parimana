from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import uvicorn
from mangum import Mangum

from parimana.app.exception import ResultNotExistError
from parimana.ui.web.model.app import AppInfo
import parimana.ui.web.router.analyse as analyse
import parimana.ui.web.router.schedule as schedule

api_router = APIRouter()
api_router.include_router(analyse.router, prefix="/analyses", tags=["analysis"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])


# health check
@api_router.get("/info")
def app_info():
    return AppInfo(status="ok")


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ResultNotExistError)
def not_exist_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=404)


def start():
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")


handler = Mangum(app)
