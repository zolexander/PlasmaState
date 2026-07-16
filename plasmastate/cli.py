from __future__ import annotations

import argparse

from . import __version__


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
        # required=True,
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
    match args.command:
        case "backup":
            print("Backup is not implemented yet.")

        case "restore":
            print("Restore is not implemented yet.")

        case "doctor":
            print("Doctor is not implemented yet.")

        case "validate":
            print("Validation is not implemented yet.")

    return 0
