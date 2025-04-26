import logging
from pathlib import Path
from typing import Annotated
import typer

from rich.console import Console

from nog.context import Context
from nog.cli import listing
from nog.cli import deletion

PROFILE_DIR = Path("/nix/var/nix/profiles")

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.WARNING)

app = typer.Typer()


@app.callback()
def main(
    ctx: typer.Context,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", "-d", help="Perform a dry run")
    ] = False,
    no_color: Annotated[
        bool, typer.Option("--no-color", help="Don't use color")
    ] = False,
):
    if no_color:
        header_color = ""
        prompt_color = ""
    else:
        header_color = "green"

        if dry_run:
            prompt_color = "yellow"
        else:
            prompt_color = "red"

    context = Context(
        console=Console(),
        profile_dir=PROFILE_DIR,
        dry_run=dry_run,
        header_color=header_color,
        prompt_color=prompt_color,
    )

    ctx.obj = {}
    ctx.obj["context"] = context


app.add_typer(listing.app)
app.add_typer(deletion.app)
