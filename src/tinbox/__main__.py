import argparse
import subprocess

from rich.console import Console
from rich.table import Table

from tinbox import config as cfg
from tinbox import fetch
from tinbox.__init__ import __version__
from tinbox.tables import get_channel_table
from tinbox.types import Video


def one_hot_vector(args: argparse.Namespace) -> list[bool]:
    # If you modify this list, make sure to update the if statement in parse() as well.
    return [
        args.inbox,
        not args.add is None,
        not args.delete is None,
        args.list,
        args.config,
    ]


def validate_args(args) -> argparse.Namespace:
    assert isinstance(args.inbox, bool), f"args.inbox is {type(args.inbox)}"
    assert isinstance(args.add, str | None), f"args.add is {type(args.add)}"
    assert isinstance(args.delete, str | None), f"args.delete is {type(args.delete)}"
    assert isinstance(args.list, bool), f"args.list is {type(args.list)}"

    is_arg_given = one_hot_vector(args)

    if sum(is_arg_given) > 1:
        raise ValueError(
            f"Only one argument can be given at a time. Received {sum(is_arg_given)}."
        )

    if sum(is_arg_given) == 0:
        args.inbox = True

    return args


def parse(args: argparse.Namespace):
    def _inbox():
        tables: list[Table] = []
        console = Console()
        for url in fetch.FEED_URLS:
            videos: list[Video] = fetch.remove_shorts(
                fetch.fetch_videos_from_channel(url)
            )
            if len(videos) == 0:
                continue
            tables.append(get_channel_table(url, videos))
        for table in tables:
            console.print(table)

    def _add():
        config = cfg.get_config()
        cfg.add_feed_url(config, args.add)
        print(f"Added {args.add} to your feeds.")

    def _delete():
        try:
            config = cfg.get_config()
            cfg.delete_feed_url(config, args.delete)
            print(f"Deleted {args.delete} from your feeds.")
        except cfg.URLNotFoundError:
            print(f"URL {args.delete} not found in your feeds.")
            return

    def _list():
        config = cfg.get_config()
        feeds = cfg.get_feed_urls(config)

        if not feeds:
            print("No feeds found. Run with -h for help.")
            return

        print(f"Your feeds: {feeds}")

    def _config():
        subprocess.run(["vim", cfg.CONFIG_PATH], check=True)

    vector = one_hot_vector(args)
    assert sum(vector) == 1, (
        f"Only one argument can be given at a time. Received {sum(vector)}"
    )

    # If you modify this, make sure to update one_hot_vector() as well.
    if vector[0]:
        _inbox()
    elif vector[1]:
        _add()
    elif vector[2]:
        _delete()
    elif vector[3]:
        _list()
    elif vector[4]:
        _config()


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="tinbox",
        description="Fetch YouTube videos from RSS feeds in your terminal.",
        epilog="Get started by adding a feed with --add",
    )
    # If you modify this, make sure to update one_hot_vector() as well.
    parser.add_argument("-i", "--inbox", action="store_true", help="get your inbox")
    parser.add_argument("-a", "--add", action="store", help="add a feed")
    parser.add_argument("-d", "--delete", action="store", help="delete a feed")
    parser.add_argument("-l", "--list", action="store_true", help="list all feeds")
    parser.add_argument(
        "-c", "--config", action="store_true", help="open config file in vim"
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()
    args = validate_args(args)
    parse(args)


if __name__ == "__main__":
    main()
