import argparse
import subprocess

from rich.console import Console
from rich.table import Table

from tinbox import config as cfg
from tinbox import fetch
from tinbox.__init__ import __version__
from tinbox.cache import clear_cache, prune_cache, save_videos_to_cache
from tinbox.tables import get_channel_table, get_feed_list_table
from tinbox.types import Video


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
    def _inbox():
        tables: list[Table] = []
        console = Console()
        for channel_name, url in zip(fetch.FEED_NAMES, fetch.FEED_URLS):
            videos: list[Video] = fetch.remove_shorts(
                fetch.fetch_videos_from_channel(url)
            )
            if len(videos) == 0:
                continue
            tables.append(
                get_channel_table(
                    channel_name,
                    videos,
                    char_limit=cfg.get_table_cols(),
                    colors=cfg.get_table_colors(),
                )
            )
            save_videos_to_cache(videos, url)
        for table in tables:
            console.print(table)

    def _add():
        cfg.add_feed(args.add[0], args.add[1])
        print(f"Added {args.add} to your feeds.")

    def _delete():
        try:
            cfg.remove_feed(feed_name=args.delete)
            print(f"Deleted {args.delete} from your feeds.")
        except cfg.FeedNameNotFoundError:
            print(f"Feed name {args.delete} not found in your feeds.")
            return

    def _list():
        if not fetch.FEED_NAMES:
            print("No feeds found. Run with -h for help.")
            return
        table: Table = get_feed_list_table(fetch.FEED_NAMES, fetch.FEED_URLS)
        console = Console()
        console.print(table)

    def _config():
        if not cfg.CONFIG_PATH.exists():
            cfg.init_config()
        subprocess.run(["vim", cfg.CONFIG_PATH], check=True)

    def _cache():
        match args.cache:
            case "prune":
                pruned: bool = prune_cache()
                if pruned:
                    print("Pruned cache.")
                else:
                    print("Cache is already pruned.")
            case "clear":
                clear_cache()
                print("Cleared cache.")
            case _:
                print(f"[error]: unrecognized command {args.cache}")

    # If you modify this, make sure to update one_hot_vector() as well.
    ARGS_TEMPLATE = (
        {"name": "inbox", "type": bool, "func": _inbox},
        {"name": "add", "type": [str, str], "func": _add},
        {"name": "delete", "type": str, "func": _delete},
        {"name": "list", "type": bool, "func": _list},
        {"name": "config", "type": bool, "func": _config},
        {"name": "cache", "type": str, "func": _cache},
    )

    vector = one_hot_vector(args)
    assert sum(vector) == 1, (
        f"Only one argument can be given at a time. Received {sum(vector)}"
    )
    ARGS_TEMPLATE[vector.index(True)]["func"]()


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
