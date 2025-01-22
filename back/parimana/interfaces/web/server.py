import uvicorn

from parimana.interfaces.web.main import app
from parimana.context import context as cx


def start():
    uvicorn.run(app, host="0.0.0.0", port=cx.settings.web_api_port, log_level="info")
