import typer
from typing import Annotated

from nog.delta import before_dt
from nog.listing import list_generations

app = typer.Typer()


@app.command()
def list(
    ctx: typer.Context,
    before: Annotated[
        str | None,
        typer.Option(
            "--before",
            "-b",
            metavar="DATE_SPEC",
            help="Only list generations before DATE_SPEC e.g. 10d. If not specified all generations will be listed.",
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
        before=before_dt(before),
        json=as_json,
    )
    list_generations(context)
