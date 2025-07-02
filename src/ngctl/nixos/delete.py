import subprocess
from operator import attrgetter

from rich.prompt import Confirm
from rich.table import Table

from ngctl.command import command_exists
from ngctl.context import Context
from ngctl.nixos.generation import system_generations


def delete_nixos_generations(context: Context) -> bool:
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

    data = system_generations(context.system_profile_dir, context.older)
    sorted_data = sorted(data, key=attrgetter("generation"), reverse=True)

    for item in sorted_data[1:]:
        tbl.add_row(*item.rich_renderables())

    context.console.print(tbl)

    if context.confirm:
        prompt = f"[{context.prompt_color}]Are you sure you wish to delete them "
        if context.user_id != 0:
            prompt += "(this requires elevated privileges) "
        prompt += "?[/]"

        ok_to_delete = Confirm.ask(
            prompt=prompt,
            console=context.console,
            default=False,
        )
    else:
        ok_to_delete = True

    deleted_ok = False
    if ok_to_delete:
        if context.user_id != 0:
            if command_exists("pkexec"):
                elevate = "pkexec"
            else:
                elevate = "sudo"

            args = [elevate, "nix-collect-garbage"]
        else:
            args = ["nix-collect-garbage"]

        if context.older_spec is None:
            args.append("--delete-old")
        else:
            args.extend(["--delete-older-than", context.older_spec])

        if not context.dry_run:
            proc = subprocess.run(args)
            if proc.returncode == 0:
                deleted_ok = True
            elif args[0] == "pkexec" and proc.returncode == 126:
                context.console.print(
                    f"[{context.prompt_color}]Generation deletion cancelled by user[/]"
                )
            elif (args[0] == "pkexec" and proc.returncode == 127) or (
                args[0] == "sudo" and proc.returncode == 1
            ):
                context.console.print(
                    f"[{context.prompt_color}]Unable to obtain required privileges to remove generations[/]"
                )
        else:
            context.console.print(f'Dry run: Would execute "{" ".join(args)}"')

    return deleted_ok
