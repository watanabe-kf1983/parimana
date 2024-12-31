from abc import ABC, abstractmethod
from typing import Callable, Collection, Sequence

from celery import Celery, Task

import parimana.tasks.decorate_util as utils

task = utils.to_be_decorated


class CeleryTasks(ABC):

    def __init__(self, celery: Celery):
        self.celery = celery

    def prepare_task(self):
        utils.decorate_methods(self, self.task_decorator)

    @abstractmethod
    def queues(self) -> Collection[str]:
        pass

    @property
    def task_decorator(self) -> Callable[[Callable], Callable]:
        return utils.compose_decorator(
            self.celery_task_decorators
            + [
                self.celery.task,
                utils.blank_decorator,  # なぜか 一つ必ず必要
            ]
            + self.task_method_decorators
        )

    @property
    def task_method_decorators(self) -> Sequence[Callable[[Callable], Callable]]:
        return []

    @property
    def celery_task_decorators(self) -> Sequence[Callable[[Task], Task]]:
        return [utils.filter_decorator(self.queue_provider, methods=["s", "si"])]

    def queue_broker(self, *args, **kwargs) -> str:
        return "default"

    def queue_provider(self, next, *args, **kwargs) -> str:
        queue_name = self.queue_broker(*args, **kwargs)
        return next(*args, queue=queue_name, **kwargs)


def route_task(name, args, kwargs, options, task=None, **kw):
    return {"queue": kwargs.get("queue")}
