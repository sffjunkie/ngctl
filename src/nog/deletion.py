import subprocess
from operator import attrgetter

from rich.prompt import Confirm
from rich.table import Table

from nog.command import command_exists
from nog.context import Context
from nog.generation import generations


def delete_generations(context: Context) -> bool:
    if context.confirm:
        context.console.print(
            f"[{context.prompt_color}]The following generations will be deleted...[/]"
        )
    else:
        context.console.print(
            f"[{context.prompt_color}]Deleting the following generations...[/]"
        )

    tbl = Table(
        "Generation",
        "Build Date",
        "NixOS Version",
        "Kernel Version",
        "Configuration Revision",
        "Specialisation",
        style=context.header_color,
        header_style=context.header_color,
    )

    data = generations(context.profile_dir, context.before)
    sorted_data = sorted(data, key=attrgetter("generation"), reverse=True)

    for item in sorted_data[1:]:
        tbl.add_row(*item.rich_renderables())

    context.console.print(tbl)

    if context.confirm:
        prompt = f"[{context.prompt_color}]Are you sure you wish to delete them (this requires elevated privileges)?[/]"

        confirm_to_delete = Confirm.ask(
            prompt=prompt,
            console=context.console,
            default=False,
        )
    else:
        confirm_to_delete = True

    delete_ok = False
    if confirm_to_delete:
        if command_exists("pkexec"):
            args = ["pkexec", "nix-collect-garbage"]
        else:
            args = ["sudo", "nix-collect-garbage"]

        if context.before is None:
            args.append("--delete-old")
        else:
            args.extend(["--delete-older-than", context.before_spec])

        if not context.dry_run:
            proc = subprocess.run(args)
            if proc.returncode == 0:
                delete_ok = True
            elif args[0] == "pkexec" and proc.returncode == 126:
                context.console.print(
                    f"[{context.prompt_color}]Generation deletion cancelled by user[/]"
                )
            elif (args[0] == "pkexec" and proc.returncode == 127) or (
                args[0] == "sudo" and proc.returncode == 1
            ):
                context.console.print(
                    f"[{context.prompt_color}]Unable to obtain required privileges to delete generations[/]"
                )
        else:
            context.console.print(f'Dry run: Would execute "{" ".join(args)}"')

    return delete_ok
