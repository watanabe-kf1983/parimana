from celery import Celery

import parimana.settings as settings

app = Celery(
    __name__, backend=settings.task_backend_uri, broker=settings.task_broker_uri
)

app.conf.event_serializer = "pickle"
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]


def run_worker():
    app.worker_main(argv=["worker", "--concurrency=1", "--loglevel=info"])
