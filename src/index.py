import feedparser

# Dummy URL from ThePrimeTime
FEED_URL = (
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCUyeluBRhGPCW4rPe_UvBZQ"
)


def fetch_videos() -> list[dict[str, str]]:
    feed = feedparser.parse(FEED_URL)
    videos = []

    for entry in feed.entries:
        videos.append(
            {
                "title": entry.title,
                "description": entry.description,
                "link": entry.link,
                "published": entry.published,
            }
        )
    return videos


def remove_videos_by_keyword(
    videos: list[dict[str, str]], keyword: str
) -> list[dict[str, str]]:
    return [
        video
        for video in videos
        if keyword not in video["title"] and keyword not in video["description"]
    ]


if __name__ == "__main__":
    videos = fetch_videos()
    videos = remove_videos_by_keyword(videos, "#short")

    for video in videos:
        print(video["title"])
