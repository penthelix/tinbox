import argparse

from tinbox import commands
from tinbox.__init__ import __version__

# If you modify this, make sure to update one_hot_vector() as well.
ARGS_TEMPLATE = (
    {"name": "inbox", "type": bool, "func": commands._inbox},
    {"name": "add", "type": [str, str], "func": commands._add},
    {"name": "delete", "type": str, "func": commands._delete},
    {"name": "list", "type": bool, "func": commands._list},
    {"name": "config", "type": bool, "func": commands._config},
    {"name": "cache", "type": str, "func": commands._cache},
)


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
    assert isinstance(args.inbox, bool), f"args.inbox is {type(args.inbox)}"
    assert isinstance(args.add, list | None), f"args.add is {type(args.add)}"
    if args.add:
        assert len(args.add) == 2 if args.add is not None else True, (
            f"args.add has length {len(args.add)}"
        )
        for i in args.add:
            assert isinstance(i, str), f"args.add[{i}] is {type(i)} instead of str"
    assert isinstance(args.delete, str | None), f"args.delete is {type(args.delete)}"
    assert isinstance(args.list, bool), f"args.list is {type(args.list)}"
    assert isinstance(args.config, bool), f"args.config is {type(args.config)}"
    assert isinstance(args.cache, str | None), f"args.cache is {type(args.cache)}"

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
    ARGS_TEMPLATE[vector.index(True)]["func"](args)


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
