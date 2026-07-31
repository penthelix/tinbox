import argparse


def validate_args(args) -> None:
    assert isinstance(args.init, bool), f"args.init is {type(args.init)}"
    assert isinstance(args.add, str | None), f"args.add is {type(args.add)}"
    assert isinstance(args.feed, list | None), f"args.feed is {type(args.feed)}"
    assert isinstance(args.delete, str | None), f"args.delete is {type(args.delete)}"
    assert isinstance(args.list, bool), f"args.list is {type(args.list)}"

    is_arg_given = [
        args.init,
        not args.feed is None,
        not args.add is None,
        not args.delete is None,
        args.list,
    ]

    if sum(is_arg_given) > 1:
        raise ValueError(
            f"Only one argument can be given at a time. Received {sum(is_arg_given)}."
        )


parser = argparse.ArgumentParser(
    prog="tinbox",
    description="Your distraction-free YouTube inbox in the terminal",
)
parser.add_argument(
    "-i", "--init", action="store_true", help="set up your %(prog)s feed"
)
parser.add_argument(
    "-f", "--feed", action="append", help="get the feed you want to read"
)
parser.add_argument("-a", "--add", action="store", help="add a feed")
parser.add_argument("-d", "--delete", action="store", help="delete a feed")
parser.add_argument("-l", "--list", action="store_true", help="list all feeds")

args = parser.parse_args()
validate_args(args)
