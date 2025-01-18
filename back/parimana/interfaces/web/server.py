import uvicorn

from parimana.interfaces.web.main import app


def start():
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
