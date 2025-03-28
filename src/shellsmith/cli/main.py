"""Main CLI entry point for shellsmith."""

import requests

from shellsmith import __version__, services
from shellsmith.config import config
from shellsmith.utils import base64_decode, base64_encode

from .commands import (
    info,
    nuke,
    shell_delete,
    submodel_delete,
    submodel_element_get,
    submodel_element_patch,
    upload,
)
from .parser import build_parser


def print_header() -> None:
    """Prints the CLI header with version and host info."""
    print("===============================================")
    print(f" Shellsmith - AAS Toolkit v{__version__}")
    print(f" Host: {config.host} ({services.health()})")
    print("===============================================")
    print()


def normalize_command_alias(cmd: str) -> str:
    """Normalizes CLI command aliases to their full form.

    Args:
        cmd: The input command or alias from the CLI.

    Returns:
        The normalized full command name.
    """
    return {
        "sh": "shell",
        "sm": "submodel",
        "sme": "submodel-element",
    }.get(cmd, cmd)


def main() -> None:
    """Parses CLI arguments and dispatches the corresponding command handler.

    This is the main entry point for the shellsmith CLI. It handles command
    alias normalization, argument parsing, and error handling.
    """
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "upload": lambda _args: upload(args.path),
        "info": lambda _args: info(),
        "nuke": lambda _args: nuke(),
        "shell.delete": lambda _args: shell_delete(args.id, cascade=args.cascade),
        "submodel.delete": lambda _args: submodel_delete(args.id, unlink=args.unlink),
        "submodel-element.get": lambda _args: submodel_element_get(args.id, args.path),
        "submodel-element.patch": lambda _args: submodel_element_patch(
            args.id, args.path, args.value
        ),
        "encode": lambda _args: print(base64_encode(args.id)),
        "decode": lambda _args: print(base64_decode(args.value)),
    }

    try:
        key = normalize_command_alias(args.command)
        if key == "shell" and args.shell_command:
            key += f".{args.shell_command}"
        elif key == "submodel" and args.submodel_command:
            key += f".{args.submodel_command}"
        elif key == "submodel-element" and args.submodel_element_command:
            key += f".{args.submodel_element_command}"

        handler = commands.get(key)
        if handler:
            if key not in ("encode", "decode"):
                print_header()
            handler(args)
        else:
            parser.print_help()
    except requests.exceptions.ConnectionError as e:
        print(f"😩 Cannot reach {config.host}: {e}")
