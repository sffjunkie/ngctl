from datetime import datetime

from pathlib import Path
from typing import NamedTuple

from rich.console import Console


class Context(NamedTuple):
    console: Console
    profile_dir: Path
    confirm: bool = True
    dry_run: bool = False
    before_spec: str | None = None
    before: datetime | None = None
    json: bool = False
    prompt_color: str = "red"
    header_color: str = "green"
