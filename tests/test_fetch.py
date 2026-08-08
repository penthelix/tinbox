from src.fetch import (
    FEED_URLS,
    fetch_videos,
    fetch_videos_from_channel,
    is_valid_youtube_url,
    remove_shorts,
)


def test_main():
    assert isinstance(FEED_URLS, set)
    for url in FEED_URLS:
        assert isinstance(url, str)
        assert url.startswith("https://www.youtube.com/feeds/videos.xml?")
        assert "channel_id=" in url


def test_is_valid_youtube_url():
    assert is_valid_youtube_url(
        "https://www.youtube.com/feeds/videos.xml?channel_id=afhjkvbsa"
    )
    assert not is_valid_youtube_url("https://www.youtube.com/watch?v=abc123")


def validate_videos_format(videos: list[dict[str, str]]) -> None:
    assert isinstance(videos, list)
    for video in videos:
        assert isinstance(video, dict)
        assert set(video.keys()) == {"title", "description", "link", "published"}
        for key in video:
            assert isinstance(video[key], str)


def test_fetch_videos():
    videos = fetch_videos()
    validate_videos_format(videos)


def test_fetch_videos_from_channel():
    videos = fetch_videos_from_channel(
        "https://www.youtube.com/feeds/videos.xml?channel_id=UCUyeluBRhGPCW4rPe_UvBZQ",
    )
    validate_videos_format(videos)


def test_remove_shorts():
    videos: list[dict[str, str]] = [
        {
            "title": "Shorts Video",
            "description": "Shorts",
            "link": "https://www.youtube.com/shorts/abc123",
            "published": "2023-01-01",
        },
        {
            "title": "Regular Video",
            "description": "Regular",
            "link": "https://www.youtube.com/watch?v=def456",
            "published": "2023-01-01",
        },
    ]

    # CONVENTION: filtered + X means that the initial list has X.
    # The thing being filtered out are shorts in all cases.
    filtered_all_videos = remove_shorts(videos)
    filtered_short = remove_shorts(videos[:1])
    filtered_video = remove_shorts(videos[1:])

    assert len(filtered_all_videos) == 1
    assert len(filtered_short) == 0
    assert len(filtered_video) == 1
    assert (
        filtered_all_videos[0]["title"] == filtered_video[0]["title"] == "Regular Video"
    )
    assert (
        type(filtered_all_videos)
        == type(filtered_short)
        == type(filtered_video)
        == list
    )
