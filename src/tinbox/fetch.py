import feedparser

from tinbox import config
from tinbox.defaults import MANDATORY_FIELDS
from tinbox.types import Video

FEED_URLS: set[str] = config.list_feed_urls()


def is_valid_youtube_url(url: str) -> bool:
    return url.startswith("https://www.youtube.com/feeds/videos.xml?channel_id=")


def fetch_videos() -> list[Video]:
    all_videos: list[Video] = []
    for url in FEED_URLS:
        videos = fetch_videos_from_channel(url)
        all_videos.extend(videos)
    return all_videos


def fetch_videos_from_channel(feed_url: str) -> list[Video]:
    feed: feedparser.FeedParserDict = feedparser.parse(feed_url)
    if not feed.entries:
        raise ValueError("No videos found in the feed.")

    videos: list[Video] = []

    for entry in feed.entries:
        for field in MANDATORY_FIELDS.get_false_values():
            if not getattr(entry, field, None):
                setattr(entry, field, "")
        missing: set[str] = {
            field
            for field in MANDATORY_FIELDS.get_true_values()
            if not getattr(entry, field, None)
        }
        if missing:
            raise ValueError(
                "Entry is missing required fields: "
                + ", ".join(missing)
                + f" for feed URL: {feed_url}"
            )

        videos.append(
            {
                "title": str(entry.title),
                "description": str(entry.description),
                "link": str(entry.link),
                "published": str(entry.published),
            }
        )
    return videos


def remove_shorts(videos: list[Video]) -> list[Video]:
    return [video for video in videos if "/shorts/" not in video["link"]]
