import argparse

import parimana.interfaces.cui.analyse as analyse_cui
import parimana.interfaces.web as web
from parimana.context import context as cx


def start_web(**kwargs):
    web.start()


def start_worker(queue_prefix: str = "", start_beat=False) -> None:
    cx.schedule_tasks.update_schedule_all().apply_async()
    cx.worker.start(queue_prefix=queue_prefix, start_beat=start_beat)


def monitor(**kwargs):
    cx.worker.start_monitor()


def main():
    parser = create_parser()
    kwargs = vars(parser.parse_args())
    if "command" in kwargs and "func" in kwargs:
        _ = kwargs.pop("command")
        func = kwargs.pop("func")
        func(**kwargs)

    else:
        parser.print_help()


def create_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="parimana", description="PARI-Mutuel betting odds ANAlyser"
    )
    subparsers = parser.add_subparsers(dest="command", help="sub commands")

    analyse_cui.add_sub_parser(subparsers)

    subparsers.add_parser("web", help="start web").set_defaults(func=start_web)
    subparsers.add_parser("monitor", help="start worker-monitor").set_defaults(
        func=monitor
    )

    worker_parser = subparsers.add_parser("worker", help="start worker")
    worker_parser.set_defaults(func=start_worker)
    worker_parser.add_argument(
        "-q",
        "--queue-prefix",
        type=str,
        default="",
        help="queue prefix",
    )
    worker_parser.add_argument(
        "-b",
        "--start-beat",
        action="store_true",
        default=False,
        help="start celery beat",
    )

    return parser
