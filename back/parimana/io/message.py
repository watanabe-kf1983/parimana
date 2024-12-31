from typing import Any, Callable, Optional
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from abc import ABC, abstractmethod
from typing import AsyncGenerator


class Channel(ABC):

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def publish(self, message: str) -> None:
        pass

    @abstractmethod
    async def alisten(self) -> AsyncGenerator[str, None]:
        pass


@dataclass
class Printer:
    channel: Optional[Channel] = None

    def mprint(self, message: Any) -> None:
        print(message)
        if c := self.channel:
            for line in str(message).splitlines():
                c.publish(line)

    def close(self) -> None:
        if c := self.channel:
            c.close()


@dataclass
class PublishCenter:
    channel_provider: Callable[[str], Channel]

    def get_channel(self, channel_id) -> Channel:
        return self.channel_provider(channel_id)

    def get_printer(self, channel_id: str):
        return Printer(self.get_channel(channel_id))

    @contextmanager
    def _set_global_printer(self, channel_id: str):
        global _global_printer
        before = _global_printer
        try:
            p = self.get_printer(channel_id)
            _global_printer = p
            yield p
        finally:
            _global_printer = before

    def with_channel_printer(self, channel_broker=None):

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                if channel_broker:
                    channel_id = channel_broker(*args, **kwargs)

                if channel_id:
                    with self._set_global_printer(channel_id) as _:
                        return func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

            return wrapper

        return decorator


_global_printer = Printer()


def mprint(msg: Any = "") -> None:
    _global_printer.mprint(msg)


def mclose() -> None:
    _global_printer.close()
