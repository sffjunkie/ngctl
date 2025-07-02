import json
from operator import attrgetter

from rich.table import Table

from ngctl.context import Context
from ngctl.hm.generation import hm_generations


def hm_list_generations(context: Context):
    tbl = Table(
        "Generation",
        "Build Date",
        "Home-Manager Version",
        header_style=context.header_color,
    )

    data = hm_generations(context.user_profile_dir, older=context.older)
    sorted_data = sorted(data, key=attrgetter("generation"), reverse=True)

    if context.json:
        print(json.dumps([g._asdict() for g in sorted_data]))
    else:
        for item in sorted_data:
            tbl.add_row(*item.rich_renderables())

        context.console.print(tbl)
