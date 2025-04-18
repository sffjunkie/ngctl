from datetime import datetime

from pathlib import Path
from typing import NamedTuple

from rich.console import Console


class Context(NamedTuple):
    console: Console
    profile_dir: Path
    confirm: bool = True
    dry_run: bool = False
    older_than_str: str | None = None
    older_than: datetime | None = None
    prompt_color: str = "red"
