from __future__ import annotations

import argparse

from . import __version__

from .command.factory import CommandFactory


from .core.context import Context

from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="plasmastate",
        description="Reproduce your KDE Plasma desktop on a fresh Linux installation.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "backup",
        help="Create a new backup.",
    )

    subparsers.add_parser(
        "restore",
        help="Restore the current system.",
    )

    subparsers.add_parser(
        "doctor",
        help="Validate the current system.",
    )

    subparsers.add_parser(
        "validate",
        help="Validate the repository.",
    )

    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return 1
    context = Context(Path.cwd())
    command = CommandFactory.create(args.command, context)
    return command.run()
