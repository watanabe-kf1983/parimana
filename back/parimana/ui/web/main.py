from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import uvicorn
from mangum import Mangum

from parimana.app.exception import ResultNotExistError
import parimana.ui.web.router.analyse as analyse
import parimana.ui.web.router.schedule as schedule

app = FastAPI()

app.include_router(analyse.router, prefix="/analyses", tags=["analysis"])
app.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
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
