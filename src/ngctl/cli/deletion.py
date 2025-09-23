import typer
from typing import Annotated

from ngctl.delta import older_dt
from ngctl.nixos.delete import delete_nixos_generations
# from ngctl.hm.delete import delete_hm_generations

app = typer.Typer()


@app.command()
def rm(
    ctx: typer.Context,
    older_spec: Annotated[
        str | None,
        typer.Option(
            "--older",
            "-o",
            metavar="DATE_SPEC",
            help="""\bOnly remove generations older than DATE_SPEC e.g. 10d.
            If not specified all previous generations will be deleted.""",
            show_default=False,
        ),
    ] = None,
    pe: Annotated[
        str | None,
        typer.Option(
            "--privilege-elevation",
            "-p",
            help="Command to elevate privileges (if not root).",
            metavar="CMD",
        ),
    ] = "pkexec",
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="Automatically accept prompts")
    ] = False,
):
    """Remove generations"""
    context = ctx.obj["context"]._replace(
        privilege_elevation=pe,
        older_spec=older_spec,
        older=older_dt(older_spec),
        confirm=not yes,
    )
    delete_nixos_generations(context)
