from dataclasses import dataclass
from functools import wraps
import time
from datetime import datetime, timedelta

from parimana.message import mprint

@dataclass
class ModestFunction:
    interval: timedelta

    def __post_init__(self):
        self.last_accessed = datetime.now() - self.interval

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delta = datetime.now() - self.last_accessed
            sleep_seconds = (self.interval - delta).total_seconds()
            if sleep_seconds > 0:
                mprint(f"waiting {sleep_seconds}secs ...")
                time.sleep(sleep_seconds)
            self.last_accessed = datetime.now()
            return func(*args, **kwargs)

        return wrapper
