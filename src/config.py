import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "tinbox" / "config.json"


def get_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config


def set_config(config: dict) -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def init_config() -> None:
    set_config(
        {
            "feed_urls": [],
        }
    )


def set_attribute(key: str, value: str | list) -> None:
    config = get_config()
    config[key] = value
    set_config(config)


def get_attribute(key: str) -> str:
    config = get_config()
    return config[key]


def get_feed_urls() -> set[str]:
    return set(get_attribute("feed_urls"))


def set_feed_urls(urls: set[str]) -> None:
    set_attribute("feed_urls", list(urls))


def add_feed_url(url: str) -> None:
    feed_urls: set[str] = get_feed_urls()
    feed_urls.add(url)
    set_feed_urls(feed_urls)


def delete_feed_url(url: str) -> None:
    feed_urls: set[str] = get_feed_urls()

    if url in feed_urls:
        feed_urls.remove(url)
        set_feed_urls(feed_urls)
    else:
        raise URLNotFoundError(f"URL {url} not found in feed_urls")


class URLNotFoundError(Exception):
    """Exception raised when a URL is not found in config feed URLs"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
