import multiprocessing
from pathlib import Path
from typing import Sequence

from parimana.tasks.base import CeleryTasks


class Worker:
    def __init__(self, tasks_list: Sequence[CeleryTasks]):
        self.celery = tasks_list[0].celery
        self.tasks_list = tasks_list

    @property
    def queues(self):
        return set(queue for tasks in self.tasks_list for queue in tasks.queues())

    def _start(self, queue_name: str):
        argv = [
            "worker",
            "--loglevel=info",
            f"--queues={queue_name}",
            "-n",
            f"worker_{queue_name}",
        ]
        if "scrape" in queue_name:
            argv.append("--concurrency=1")

        self.celery.worker_main(argv)

    def _start_beat(self):
        celerybeat_tmppath = Path("/tmp/parimana/celery/celerybeat-schedule")
        celerybeat_tmppath.parent.mkdir(parents=True, exist_ok=True)
        argv = [
            "beat",
            "--loglevel=info",
            "-s",
            str(celerybeat_tmppath),
        ]
        self.celery.start(argv)

    def start(self, queue_prefix: str = "", start_beat: bool = False):

        workers = [
            multiprocessing.Process(
                name=f"Worker_for_{queue}", target=self._start, args=[queue]
            )
            for queue in self.queues
            if queue.startswith(queue_prefix)
        ]
        if start_beat:
            workers.append(
                multiprocessing.Process(name="Celery_Beat", target=self._start_beat)
            )

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

    def start_monitor(self):

        argv = ["flower"]
        self.celery.start(argv)
