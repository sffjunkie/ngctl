import json
from operator import attrgetter

from rich.table import Table

from nog.context import Context
from nog.generation import generations


def list_generations(context: Context):
    tbl = Table(
        "Generation",
        "Build Date",
        "NixOS Version",
        "Kernel Version",
        "Configuration Revision",
        "Specialisation",
        header_style=context.header_color,
    )

    data = generations(context.profile_dir, before=context.before)
    sorted_data = sorted(data, key=attrgetter("generation"), reverse=True)

    if context.json:
        print(json.dumps([g._asdict() for g in sorted_data]))
    else:
        for item in sorted_data:
            tbl.add_row(*item.rich_renderables())

        context.console.print(tbl)
