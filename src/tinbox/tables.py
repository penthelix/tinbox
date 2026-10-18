from rich.table import Table

from tinbox.types import VIDEO_FORMAT, Video


def get_channel_table(
    channel_name: str, channel_videos: list[Video], char_limit: int = 40
) -> Table:
    """
    Returns a rich.table.Table for a channel with the videos in the channel.

    The columns are the keys of the VIDEO_FORMAT dictionary. The rows are the videos in
    the channel.
    """
    table = Table(title=channel_name)

    for key in VIDEO_FORMAT():
        table.add_column(key)

    for video in channel_videos:
        table.add_row(*[str(video[key])[:char_limit] for key in VIDEO_FORMAT()])

    return table


def get_feed_tables(feed: dict[str, list[Video]]) -> list[Table]:
    """Returns a list of rich.table.Table for each channel in the feed."""
    return [
        get_channel_table(channel_name, videos) for channel_name, videos in feed.items()
    ]
