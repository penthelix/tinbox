#!/usr/bin/env python3
import argparse

from src import config, fetch


def one_hot_vector(args: argparse.Namespace) -> list[bool]:
    return [
        args.feed,
        not args.add is None,
        not args.delete is None,
        args.list,
    ]


def validate_args(args) -> argparse.Namespace:
    assert isinstance(args.add, str | None), f"args.add is {type(args.add)}"
    assert isinstance(args.feed, bool), f"args.feed is {type(args.feed)}"
    assert isinstance(args.delete, str | None), f"args.delete is {type(args.delete)}"
    assert isinstance(args.list, bool), f"args.list is {type(args.list)}"

    is_arg_given = one_hot_vector(args)

    if sum(is_arg_given) > 1:
        raise ValueError(
            f"Only one argument can be given at a time. Received {sum(is_arg_given)}."
        )

    if sum(is_arg_given) == 0:
        args.feed = True

    return args


def parse(args: argparse.Namespace):
    def _feed():
        videos = fetch.fetch_videos()
        videos = fetch.remove_shorts(videos)

        print(f"Found {len(videos)} videos from {len(fetch.FEED_URLS)}")
        for video in videos:
            print(video["title"])

    def _add():
        config.add_feed_url(args.add)
        print(f"Added {args.add} to your feeds.")

    def _delete():
        try:
            config.delete_feed_url(args.delete)
            print(f"Deleted {args.deleted} from your feeds.")
        except config.URLNotFoundError:
            print(f"URL {args.delete} not found in your feeds.")
            return

    def _list():
        feeds = config.get_feed_urls()
        print(f"Your feeds: {feeds}")

    vector = one_hot_vector(args)
    assert sum(vector) == 1, (
        f"Only one argument can be given at a time. Received {sum(vector)}"
    )

    if vector[0]:
        _feed()
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
    )
    parser.add_argument(
        "-f", "--feed", action="store_true", help="get the feed you want to read"
    )
    parser.add_argument("-a", "--add", action="store", help="add a feed")
    parser.add_argument("-d", "--delete", action="store", help="delete a feed")
    parser.add_argument("-l", "--list", action="store_true", help="list all feeds")

    args = parser.parse_args()
    args = validate_args(args)
    parse(args)
    input()
