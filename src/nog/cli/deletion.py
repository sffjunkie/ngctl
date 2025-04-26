import typer
from typing import Annotated

from nog.delta import before_dt
from nog.deletion import delete_generations

app = typer.Typer()


@app.command()
def delete(
    ctx: typer.Context,
    before: Annotated[
        str | None,
        typer.Option(
            "--before",
            "-b",
            metavar="DATE_SPEC",
            help="Only delete generations before DATE_SPEC e.g. 10d. If not specified all previous generations will be deleted.",
            show_default=False,
        ),
    ] = None,
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="Automatically accept prompts")
    ] = False,
):
    """Delete generations"""
    context = ctx.obj["context"]._replace(
        before=before_dt(before),
        confirm=not yes,
    )
    delete_generations(context)
