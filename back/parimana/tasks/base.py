from abc import ABC, abstractmethod
from functools import wraps
from typing import Collection
from celery import Celery
from parimana.io.message import PublishCenter


_TASK_FUNC_ATTR = "_is_celery_task"


def task(func):
    setattr(func, _TASK_FUNC_ATTR, True)
    return func


def add_queue(func):
    @wraps(func)
    def wrapper(*args, queue: str = "default", **kwargs):
        return func(*args, **kwargs)

    return wrapper


def route_task(name, args, kwargs, options, task=None, **kw):
    return {"queue": kwargs.get("queue")}


class CeleryTasks(ABC):

    def __init__(self, celery: Celery, publish_center: PublishCenter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.celery = celery
        for attr_name in dir(self):
            if not attr_name.startswith("__"):
                attr = getattr(self, attr_name)
                if callable(attr) and getattr(attr, _TASK_FUNC_ATTR, False):
                    task_func = publish_center.with_channel_printer(add_queue(attr))
                    setattr(self, attr_name, celery.task(task_func))

    @abstractmethod
    def queues(self) -> Collection[str]:
        pass
