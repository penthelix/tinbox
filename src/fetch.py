import feedparser

from src import config as cfg

config: cfg.Config = {}
try:
    config = cfg.get_config()
except FileNotFoundError:
    cfg.init_config()
    config = cfg.get_config()
finally:
    FEED_URLS: set[str] = cfg.get_feed_urls(config)


def is_valid_youtube_url(url: str) -> bool:
    return url.startswith("https://www.youtube.com/feeds/videos.xml?channel_id=")


def fetch_videos() -> list[dict[str, str]]:
    all_videos: list[dict[str, str]] = []
    for url in FEED_URLS:
        videos = fetch_videos_from_channel(url)
        all_videos.extend(videos)
    return all_videos


def fetch_videos_from_channel(feed_url: str) -> list[dict[str, str]]:
    feed: feedparser.FeedParserDict = feedparser.parse(feed_url)
    if not feed.entries:
        raise ValueError("No videos found in the feed.")

    videos: list[dict[str, str]] = []

    for entry in feed.entries:
        missing: list[str] = [
            field
            for field in ["title", "description", "link", "published"]
            if not getattr(entry, field, None)
        ]
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


def remove_shorts(videos: list[dict[str, str]]) -> list[dict[str, str]]:
    return [video for video in videos if "/shorts/" not in video["link"]]
