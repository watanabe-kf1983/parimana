import argparse

import parimana.ui.cui.analyse as analyse_cui
import parimana.ui.web as web
import parimana.context as cx


def init_today(args) -> None:
    cx.schedule_tasks.init_today().apply()


def start_web(args):
    web.start()


def worker(args):
    cx.worker.start()


def monitor(args):
    cx.worker.start_monitor()


def main():
    parser = create_parser()
    args = vars(parser.parse_args())
    if "command" in args and "func" in args:
        _ = args.pop("command")
        func = args.pop("func")
        func(args)

    else:
        parser.print_help()


def create_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="parimana", description="PARI-Mutuel betting odds ANAlyser"
    )
    subparsers = parser.add_subparsers(dest="command", help="sub commands")

    analyse_cui.add_sub_parser(subparsers)

    subparsers.add_parser("web", help="start web").set_defaults(func=start_web)
    subparsers.add_parser("init", help="init today").set_defaults(func=init_today)
    subparsers.add_parser("worker", help="start worker").set_defaults(func=worker)
    subparsers.add_parser("monitor", help="start worker-monitor").set_defaults(
        func=monitor
    )

    return parser
