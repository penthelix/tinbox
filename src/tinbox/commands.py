import subprocess
from argparse import Namespace

from rich.console import Console
from rich.table import Table

from tinbox import config as cfg
from tinbox import fetch
from tinbox.cache import clear_cache, prune_cache, save_videos_to_cache
from tinbox.tables import get_channel_table, get_feed_list_table
from tinbox.types import Video


def _inbox(_):
    tables: list[Table] = []
    console = Console()
    for channel_name, url in zip(fetch.FEED_NAMES, fetch.FEED_URLS):
        videos: list[Video] = fetch.remove_shorts(fetch.fetch_videos_from_channel(url))
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


def _add(args: Namespace):
    cfg.add_feed(args.add[0], args.add[1])
    print(f"Added {args.add} to your feeds.")


def _delete(args: Namespace):
    try:
        cfg.remove_feed(feed_name=args.delete)
        print(f"Deleted {args.delete} from your feeds.")
    except cfg.FeedNameNotFoundError:
        print(f"Feed name {args.delete} not found in your feeds.")
        return


def _list(_):
    if not fetch.FEED_NAMES:
        print("No feeds found. Run with -h for help.")
        return
    table: Table = get_feed_list_table(fetch.FEED_NAMES, fetch.FEED_URLS)
    console = Console()
    console.print(table)


def _config(_):
    if not cfg.CONFIG_PATH.exists():
        cfg.init_config()
    subprocess.run(["vim", cfg.CONFIG_PATH], check=True)


def _cache(args: Namespace):
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
