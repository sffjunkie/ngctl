import argparse
import logging
from pathlib import Path
from datetime import datetime

from rich.console import Console

from nog.context import Context
from nog.garbage import garbage_collect
from nog.deletion import delete_generations
from nog.listing import list_generations
from nog.delta import older_offset_unit, older_timedelta

PROFILE_DIR = Path("/nix/var/nix/profiles")

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.WARNING)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Perform a dry run",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Don't use color",
    )
    subparsers = parser.add_subparsers(
        dest="subcommand",
        title="Commands",
        help="NixOS Garbage Manager",
    )

    subparsers.add_parser("gc", help="Garbage collect")
    list_parser = subparsers.add_parser("list", help="List generations")
    delete_parser = subparsers.add_parser("delete", help="Delete generations")

    list_parser.add_argument(
        "-o", "--older", metavar="THAN", help="Older than", default=None
    )
    list_parser.add_argument("-a", "--all", action="store_true", default=False)

    delete_parser.add_argument(
        "-o", "--older", metavar="THAN", help="Older than", default=None
    )
    delete_parser.add_argument("-a", "--all", action="store_true", default=False)
    delete_parser.add_argument("-y", "--yes", action="store_true", default=False)

    args = parser.parse_args()

    if args.older is None or args.all:
        older_than_str = None
    else:
        older_than_str = args.older

    if args.dry_run:
        if args.no_color:
            prompt_color = ""
        else:
            prompt_color = "yellow"
    else:
        if args.no_color:
            prompt_color = ""
        else:
            prompt_color = "red"

    ctx = Context(
        confirm=not args.yes,
        profile_dir=PROFILE_DIR,
        console=Console(),
        dry_run=args.dry_run,
        older_than_str=older_than_str,
        prompt_color=prompt_color,
    )

    offset_unit = older_offset_unit(ctx.older_than_str)
    if offset_unit is None:
        older_than = None
    else:
        offset, unit = offset_unit

        dt = older_timedelta(offset, unit)
        if dt is not None:
            older_than = datetime.now() - dt
        else:
            older_than = None

    ctx = ctx._replace(older_than=older_than)

    if args.subcommand is None:
        parser.print_help()
    elif args.subcommand == "gc":
        garbage_collect(context=ctx)
    elif args.subcommand == "list":
        list_generations(context=ctx)
    elif args.subcommand == "delete":
        delete_generations(context=ctx)


if __name__ == "__main__":
    main()
