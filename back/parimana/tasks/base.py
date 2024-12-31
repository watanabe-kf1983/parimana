from abc import ABC, abstractmethod
from typing import Callable, Collection, Optional, Sequence

from celery import Celery

from parimana.io.message import PublishCenter
import parimana.tasks.decorate_util as utils

task = utils.to_be_decorated


class CeleryTasks(ABC):

    def __init__(self, celery: Celery, publish_center: PublishCenter):
        self.celery = celery
        self.publish_center = publish_center

        utils.decorate(self, self.task_decorator)

    @abstractmethod
    def queues(self) -> Collection[str]:
        pass

    @property
    def task_decorator(self) -> Callable[[Callable], Callable]:
        return utils.compose_decorator(self.task_decorators)

    @property
    def task_decorators(self) -> Sequence[Callable[[Callable], Callable]]:
        return [
            self.celery.task,
            self.publish_center.with_channel_printer(self.channel_broker),
        ]

    def channel_broker(self, *args, **kwargs) -> Optional[str]:
        return kwargs.get("channel_id")


def route_task(name, args, kwargs, options, task=None, **kw):
    return {"queue": kwargs.get("queue")}
