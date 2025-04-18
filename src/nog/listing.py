from datetime import datetime
from operator import attrgetter

from rich.console import Console
from rich.table import Table

from nog.context import Context
from nog.delta import older_offset_unit, older_timedelta
from nog.generation import generations


def list_generations(
    context: Context,
):
    c = Console()
    tbl = Table(
        "Generation",
        "Build Date",
        "NixOS Version",
        "Kernel Version",
        "Configuration Revision",
        "Specialisation",
    )

    offset_unit = older_offset_unit(context.older_than)
    if offset_unit is None:
        before = None
    else:
        offset, unit = offset_unit

        dt = older_timedelta(offset, unit)
        if dt is not None:
            before = datetime.now() - dt
        else:
            before = None

    data = generations(context.profile_dir, before)

    for item in sorted(data, key=attrgetter("number"), reverse=True):
        if item.current:
            tbl.add_row(item.number + " current", *item[1:-1])
        else:
            tbl.add_row(*item[:-1])

    c.print(tbl)
