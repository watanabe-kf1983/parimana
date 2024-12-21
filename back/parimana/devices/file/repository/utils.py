from pathlib import Path
import pickle
from typing import Optional

import plotly.io as pio

from parimana.utils.message import mprint


def read_text(file_path: Path) -> Optional[str]:
    if file_path.exists():
        with open(file_path, "r") as f:
            return f.read()
    else:
        return None


def write_text(file_path: Path, txt: str) -> None:
    with open(file_path, "w") as f:
        f.write(txt)


def write_html_chart(file_path: Path, chart_json: str) -> None:
    chart = pio.from_json(chart_json)
    html = chart.to_html(include_plotlyjs="cdn", include_mathjax="cdn")
    write_text(file_path, html)


def read_pickle(file_path: Path):
    if file_path.exists():
        mprint(f"reading {file_path}...")
        with open(file_path, "rb") as f:
            return pickle.load(f)
    else:
        return None


def write_as_pickle(file_path: Path, obj):
    with open(file_path, "wb") as f:
        mprint(f"writing {file_path}...")
        pickle.dump(obj, f)


def write_bytes(file_path: Path, binary: bytes):
    with open(file_path, "wb") as f:
        mprint(f"writing {file_path}...")
        f.write(binary)
