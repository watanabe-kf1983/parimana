from celery import Celery
import parimana.settings as settings


app = Celery(__name__, config_source="parimana.tasks.celeryconfig")

_publisher = settings.publish_center


def task(func):
    return app.task(_publisher.with_channel_printer(func))


def run_worker():
    app.worker_main(argv=["worker", "--concurrency=1", "--loglevel=info"])
