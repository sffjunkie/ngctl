import json
from operator import attrgetter

from rich.table import Table

from ngctl.context import Context
from ngctl.nixos.generation import system_generations


def system_list_generations(context: Context):
    tbl = Table(
        "Generation\n",
        "Build\nDate",
        "NixOS\nVersion",
        "Kernel\nVersion",
        "Configuration\nRevision",
        "Specialisation\n",
        header_style=context.header_color,
    )

    data = system_generations(context.system_profile_dir, older=context.older)
    sorted_data = sorted(data, key=attrgetter("generation"), reverse=True)

    if context.json:
        print(json.dumps([g._asdict() for g in sorted_data]))
    else:
        for item in sorted_data:
            tbl.add_row(*item.rich_renderables())

        context.console.print(tbl)
