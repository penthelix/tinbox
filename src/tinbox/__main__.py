import argparse

from src import config as cfg
from src import fetch


def one_hot_vector(args: argparse.Namespace) -> list[bool]:
    # If you modify this list, make sure to update the if statement in parse() as well.
    return [
        args.inbox,
        not args.add is None,
        not args.delete is None,
        args.list,
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
        videos = fetch.fetch_videos()
        videos = fetch.remove_shorts(videos)

        if len(videos) == 0:
            print("No videos in inbox. Run with -h for help.")
            return

        print(f"Found {len(videos)} videos from {len(fetch.FEED_URLS)} feeds.")
        for video in videos:
            print(video["title"])

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


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="tinbox",
        description="Your distraction-free YouTube inbox in the terminal",
        epilog="Get started by adding a feed with --add",
    )
    parser.add_argument("-i", "--inbox", action="store_true", help="get your inbox")
    parser.add_argument("-a", "--add", action="store", help="add a feed")
    parser.add_argument("-d", "--delete", action="store", help="delete a feed")
    parser.add_argument("-l", "--list", action="store_true", help="list all feeds")

    args = parser.parse_args()
    args = validate_args(args)
    parse(args)
