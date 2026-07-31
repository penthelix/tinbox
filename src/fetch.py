import feedparser

from config import get_feed_urls

FEED_URLS: set[str] = get_feed_urls()


def fetch_videos() -> list[dict[str, str]]:
    all_videos: list[dict[str, str]] = []
    for url in FEED_URLS:
        videos = fetch_videos_from_channel(url)
        all_videos.extend(videos)
    return all_videos


def fetch_videos_from_channel(feed_url) -> list[dict[str, str]]:
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        raise ValueError("No videos found in the feed.")

    videos: list[dict[str, str]] = []

    for entry in feed.entries:
        missing = [
            field
            for field in ["title", "description", "link", "published"]
            if not getattr(entry, field, None)
        ]
        if missing:
            raise ValueError(
                "Entry is missing required fields: "
                + ", ".join(missing)
                + f"for feed URL: {feed_url}"
            )

        videos.append(
            {
                "title": entry.title,
                "description": entry.description,
                "link": entry.link,
                "published": entry.published,
            }
        )
    return videos


def remove_shorts(videos: list[dict[str, str]]) -> list[dict[str, str]]:
    return [video for video in videos if "/shorts/" not in video["link"]]


def remove_videos_by_keyword(
    videos: list[dict[str, str]], keyword: str
) -> list[dict[str, str]]:
    if not keyword:
        raise ValueError("Keyword cannot be empty.")

    keyword = keyword.lower()
    title: str = video["title"].lower()
    description: str = video["description"].lower()

    return [
        video for video in videos if keyword not in title and keyword not in description
    ]


if __name__ == "__main__":
    videos = fetch_videos()
    videos = remove_shorts(videos)

    for video in videos:
        print(video["title"])
