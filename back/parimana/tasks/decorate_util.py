from typing import Callable, Sequence

from toolz import compose

_DECO_FUNC_ATTR = "_to_be_decorated"


def to_be_decorated(func):
    setattr(func, _DECO_FUNC_ATTR, True)
    return func


def _is_to_be_decorated(func):
    return callable(func) and getattr(func, _DECO_FUNC_ATTR, False)


def decorate(obj: object, decorator: Callable[[Callable], Callable]):
    for attr_name in dir(obj):
        attr = getattr(obj, attr_name)
        if _is_to_be_decorated(attr):
            setattr(obj, attr_name, decorator(attr))


def compose_decorator(
    decorators: Sequence[Callable[[Callable], Callable]]
) -> Callable[[Callable], Callable]:

    return compose(*decorators)
