import functools
from typing import Callable, Generic, Optional, Sequence, TypeVar

from toolz import compose

_DECO_FUNC_ATTR = "_to_be_decorated"


def to_be_decorated(func):
    setattr(func, _DECO_FUNC_ATTR, True)
    return func


def _is_to_be_decorated(func):
    return callable(func) and getattr(func, _DECO_FUNC_ATTR, False)


def decorate_methods(obj: object, decorator: Callable[[Callable], Callable]):
    for attr_name in dir(obj):
        attr = getattr(obj, attr_name)
        if _is_to_be_decorated(attr):
            setattr(obj, attr_name, decorator(attr))


def compose_decorator(
    decorators: Sequence[Callable[[Callable], Callable]]
) -> Callable[[Callable], Callable]:

    return compose(*decorators)


def blank_decorator(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


T = TypeVar("T")


class Proxy(Generic[T]):
    def __init__(self, target: T, *, intercept: Sequence[str], filter: Callable):
        self._target = target
        self._filter = filter
        self._intercept = intercept

    def __getattr__(self, name: str):
        attr = getattr(self._target, name)
        if name in self._intercept:
            return filter_func_decorator(self._filter)(attr)
        else:
            return attr


def filter_decorator(filter: Callable, *, methods: Optional[Sequence[str]] = None):
    if methods:

        def deco(obj):
            return Proxy(obj, intercept=methods, filter=filter)

        return deco
    else:
        return filter_func_decorator(filter)


def filter_func_decorator(filter: Callable):

    def deco(func):

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return filter(func, *args, **kwargs)

        return wrapped

    return deco
