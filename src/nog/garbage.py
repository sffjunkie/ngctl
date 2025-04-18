import subprocess
from rich.prompt import Confirm

from nog.context import Context


def garbage_collect(
    ctx: Context,
):
    if ctx.confirm:
        prompt = f"[{ctx.color}]Are you sure you wish to delete them (this requires elevated privileges)?[/]"

        confirm_to_delete = Confirm.ask(
            prompt=prompt,
            console=ctx.console,
            default=False,
        )
    else:
        confirm_to_delete = True

    if not ctx.dry_run and confirm_to_delete:
        proc = subprocess.run(["nix-collect-garbage"])
        if proc.returncode == 0:
            pass
