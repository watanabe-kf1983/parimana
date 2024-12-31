import multiprocessing
from typing import Sequence

from parimana.tasks.base import CeleryTasks


class Worker:
    def __init__(self, tasks_list: Sequence[CeleryTasks]):
        self.celery = tasks_list[0].celery
        self.queues = set(queue for tasks in tasks_list for queue in tasks.queues())

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

    def start(self):

        workers = [
            multiprocessing.Process(
                name=f"Worker_for_{queue}", target=self._start, args=[queue]
            )
            for queue in self.queues
        ]

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

    def start_monitor(self):

        argv = ["flower"]
        self.celery.start(argv)
