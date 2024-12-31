from abc import ABC, abstractmethod
from typing import Callable, Collection, Sequence

from celery import Celery

import parimana.tasks.decorate_util as utils

task = utils.to_be_decorated


class CeleryTasks(ABC):

    def __init__(self, celery: Celery):
        self.celery = celery

    def prepare_task(self):
        utils.decorate(self, self.task_decorator)

    @abstractmethod
    def queues(self) -> Collection[str]:
        pass

    @property
    def task_decorator(self) -> Callable[[Callable], Callable]:
        return utils.compose_decorator(
            [
                self.celery.task,
                utils.blank_decorator,  # なぜか 一つ必ず必要
            ]
            + self.task_method_decorators
        )

    @property
    def task_method_decorators(self) -> Sequence[Callable[[Callable], Callable]]:
        return []


def route_task(name, args, kwargs, options, task=None, **kw):
    return {"queue": kwargs.get("queue")}
