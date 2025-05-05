from datetime import datetime

from pathlib import Path
from typing import NamedTuple

from rich.console import Console


class Context(NamedTuple):
    user_id: int
    user_name: str
    console: Console
    system_profile_dir: Path
    hm_profile_dir: Path
    privilege_elevation: str = "pkexec"
    confirm: bool = True
    dry_run: bool = False
    older_spec: str | None = None
    older: datetime | None = None
    json: bool = False
    prompt_color: str = "red"
    header_color: str = "green"
