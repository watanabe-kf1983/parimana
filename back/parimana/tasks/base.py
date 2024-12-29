from celery import Celery
from parimana.io.message import PublishCenter


_TASK_FUNC_ATTR = "_is_celery_task"


def task(func):
    setattr(func, _TASK_FUNC_ATTR, True)
    return func


class CeleryTasks:

    def __init__(self, celery: Celery, publish_center: PublishCenter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr_name in dir(self):
            if not attr_name.startswith("__"):
                attr = getattr(self, attr_name)
                if callable(attr) and getattr(attr, _TASK_FUNC_ATTR, False):
                    setattr(
                        self,
                        attr_name,
                        celery.task(publish_center.with_channel_printer(attr)),
                    )


class Worker:
    def __init__(self, celery: Celery):
        self.celery = celery

    def start(self):
        self.celery.worker_main(argv=["worker", "--concurrency=1", "--loglevel=info"])
