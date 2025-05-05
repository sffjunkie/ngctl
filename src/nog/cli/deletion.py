import typer
from typing import Annotated

from nog.delta import older_dt
from nog.delete_nixos import delete_nixos_generations
# from nog.delete_hm import delete_hm_generations

app = typer.Typer()


@app.command()
def delete(
    ctx: typer.Context,
    older_spec: Annotated[
        str | None,
        typer.Option(
            "--older",
            "-o",
            metavar="DATE_SPEC",
            help="""\bOnly delete generations older than DATE_SPEC e.g. 10d.
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
    """Delete generations"""
    context = ctx.obj["context"]._replace(
        privelege_elevation=pe,
        older_spec=older_spec,
        older=older_dt(older_spec),
        confirm=not yes,
    )
    delete_nixos_generations(context)
