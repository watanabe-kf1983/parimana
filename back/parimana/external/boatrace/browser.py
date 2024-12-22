import functools
from datetime import timedelta

import requests

from parimana.io.message import mprint
from parimana.external.scraping_utils.modest import ModestFunction


modestly = ModestFunction(interval=timedelta(seconds=1.5))


@functools.cache
@modestly
def get(uri: str, attempt: str):
    mprint(f"opening {uri} ...")
    res = requests.get(uri)
    res.raise_for_status()
    text = res.text
    return text
