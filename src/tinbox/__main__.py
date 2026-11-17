import argparse
from collections.abc import Callable
from typing import Any, TypedDict

from tinbox.__init__ import __version__
from tinbox.commands import _add, _cache, _config, _delete, _inbox, _list


# If you modify this, make sure to update one_hot_vector() as well.
class ArgsTemplateTemplate(TypedDict):
    command: tuple[str, ...]
    type: tuple[type, ...]
    func: tuple[Callable, ...]
    len: tuple[int, ...]


# If you modify this, make sure to update one_hot_vector() as well.
ARGS_TEMPLATE: ArgsTemplateTemplate = {
    "command": ("inbox", "add", "delete", "list", "config", "cache"),
    "type": (bool, tuple, str, bool, bool, str),
    "func": (_inbox, _add, _delete, _list, _config, _cache),
    "len": (-1, 2, -1, -1, -1, -1),
}
COMMANDS = ARGS_TEMPLATE["command"]


def get_attr_from_command(command: str, attr: str) -> Any:
    if command not in COMMANDS:
        raise ValueError(f"command {command} not in {COMMANDS}")
    if not attr in ARGS_TEMPLATE:
        raise ValueError(f"attr {attr} not in {ARGS_TEMPLATE.keys()}")
    if attr == "command":
        raise ValueError("attr cannot be 'command'.")
    return ARGS_TEMPLATE[attr][ARGS_TEMPLATE["command"].index(command)]


def one_hot_vector(args: argparse.Namespace) -> list[bool]:
    # If you modify this list, make sure to update the if statement in parse() as well.
    return [
        args.inbox,
        not args.add is None,
        not args.delete is None,
        args.list,
        args.config,
        not args.cache is None,
    ]


def validated_args(args: argparse.Namespace) -> argparse.Namespace:
    for command in COMMANDS:
        required_type: type = get_attr_from_command(command=command, attr="type")
        if isinstance(getattr(args, command), required_type):
            continue
        if required_type is not bool and getattr(args, command) is None:
            continue
        try:
            setattr(args, command, required_type(getattr(args, command)))
        except TypeError, ValueError:
            assert isinstance(getattr(args, command), required_type), (
                f"args.{command} is {type(getattr(args, command))} instead of {required_type}"
            )
    # TODO: Set this up within the template
    if isinstance(args.add, list):
        assert len(args.add) == get_attr_from_command(command="add", attr="len"), (
            f"args.add has length {len(args.add)}"
        )
        for i in args.add:
            assert isinstance(i, str), f"args.add[{i}] is {type(i)} instead of str"

    vector = one_hot_vector(args)
    if sum(vector) > 1:
        raise ValueError(
            f"Only one argument can be given at a time. Received {sum(vector)}."
        )
    if sum(vector) == 0:
        args.inbox = True
    return args


def parse(args: argparse.Namespace):
    vector = one_hot_vector(args)
    assert sum(vector) == 1, (
        f"Only one argument can be given at a time. Received {sum(vector)}"
    )
    ARGS_TEMPLATE["func"][vector.index(True)](args)


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="tinbox",
        description="Fetch YouTube videos from RSS feeds in your terminal.",
        epilog="Get started by adding a feed with --add",
    )
    # If you modify this, make sure to update one_hot_vector() as well.
    parser.add_argument("-i", "--inbox", action="store_true", help="get your inbox")
    parser.add_argument("-a", "--add", action="extend", nargs=2, help="add a feed")
    parser.add_argument("-d", "--delete", action="store", help="delete a feed")
    parser.add_argument("-l", "--list", action="store_true", help="list all feeds")
    parser.add_argument(
        "-c", "--config", action="store_true", help="open config file in vim"
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("--cache", action="store", help="prune/clear cache")

    args = parser.parse_args()
    args = validated_args(args)
    parse(args)


if __name__ == "__main__":
    main()
