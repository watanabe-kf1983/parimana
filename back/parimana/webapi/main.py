from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import uvicorn

from parimana.webapi import router
import parimana.app.realtime as rt

app = FastAPI()

app.include_router(router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
    ],
)


@app.exception_handler(rt.ResultNotExistError)
def not_exist_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=404)


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


if __name__ == "__main__":
    start()
