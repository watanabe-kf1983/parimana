from contextlib import contextmanager
from functools import wraps
import traceback
from typing import Any

from parimana.infra.message.redis import Channel


class Printer:
    def __init__(self, channel_id: str | None = None):
        self.channel_id = channel_id
        self.channel: Channel | None = None
        if self.channel_id:
            try:
                self.channel = Channel(self.channel_id).pingged()
            except Exception:
                self.channel = None

    def mprint(self, message: Any) -> None:
        print(message)
        if c := self.channel:
            for line in str(message).splitlines():
                c.publish(line)

    def close(self) -> None:
        if c := self.channel:
            c.close()


@contextmanager
def set_printer(channel_id: str):
    global _global_printer
    before = _global_printer
    try:
        p = Printer(channel_id)
        _global_printer = p
        yield p
    finally:
        _global_printer = before


def with_channel_printer(func):
    @wraps(func)
    def wrapper(*args, channel_id: str, **kwargs):

        with set_printer(channel_id) as _:
            return func(*args, **kwargs)

    return wrapper


_global_printer = Printer()


def mprint(msg: str = "") -> None:
    _global_printer.mprint(msg)


def mclose() -> None:
    _global_printer.close()
