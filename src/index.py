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


def remove_shorts(videos: list[dict[str, str]]) -> list[dict[str, str]]:
    return [video for video in videos if "/shorts/" not in video["link"]]


def remove_videos_by_keyboard(
    videos: list[dict[str, str]], keyword: str
) -> list[dict[str, str]]:
    if not keyword:
        raise ValueError("Keyword cannot be empty.")

    keyword = keyword.lower()
    title = video["title"].lower()
    description = video["description"].lower()

    return [
        video for video in videos if keyword not in title and keyword not in description
    ]


if __name__ == "__main__":
    videos = fetch_videos()
    videos = remove_shorts(videos)

    for video in videos:
        print(video["title"])
