from rich.table import Table

from tinbox.defaults import TABLE_COLORS, TABLE_COLS
from tinbox.types import Video, VideoFormat


def get_channel_table(
    channel_name: str,
    channel_videos: list[Video],
    char_limit: VideoFormat[int] = TABLE_COLS,
    colors: VideoFormat = TABLE_COLORS,
) -> Table:
    """
    Returns a rich.table.Table for a channel with the videos in the channel.

    The columns are the keys of the VIDEO_FORMAT dictionary. The rows are the videos in
    the channel.

    Args:
        channel_name (str): Title of the table
        channel_videos (list[Video]): The rows of the table
        char_limit (VideoFormat[int], optional): The maximum number of characters to
            display in a cell. Defaults to defaults.TABLE_COLS.
        colors (VideoFormat): The colors to use for the columns. Defaults to
            defaults.TABLE_COLORS.
    """
    if not colors:
        colors = VideoFormat()

    table = Table(title=channel_name)

    for key in VideoFormat():
        table.add_column(key, style=colors[key])

    for video in channel_videos:
        table.add_row(*[str(video[key])[: char_limit[key]] for key in VideoFormat()])

    return table


def get_feed_tables(feed: dict[str, list[Video]]) -> list[Table]:
    """Returns a list of rich.table.Table for each channel in the feed."""
    return [
        get_channel_table(channel_name, videos) for channel_name, videos in feed.items()
    ]
