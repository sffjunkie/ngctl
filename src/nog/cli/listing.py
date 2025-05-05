import typer
from typing import Annotated

from nog.delta import older_dt
from nog.nixos.listing import list_generations

app = typer.Typer()


@app.command()
def list(
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
    as_json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="List generations as JSON",
        ),
    ] = None,
):
    """List Generations"""

    context = ctx.obj["context"]._replace(
        older_spec=older_spec,
        older=older_dt(older_spec),
        json=as_json,
    )
    list_generations(context)
