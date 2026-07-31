import argparse

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

parser.print_help()
