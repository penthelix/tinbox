import json
from pathlib import Path

type Config = dict[str, str | list[str]]

CONFIG_PATH: Path = Path.home() / ".config" / "tinbox" / "config.json"
CONFIG_FORMAT: Config = {"feed_urls": []}


def get_config(config_path: str | Path = CONFIG_PATH) -> Config:
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

    with open(config_path, "r") as f:
        config = json.load(f)
    return config


def set_config(config: Config, config_path: str | Path = CONFIG_PATH) -> None:
    config_path = Path(config_path)
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.touch()

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


def init_config(config_path: str | Path = CONFIG_PATH) -> None:
    config_path = Path(config_path)
    set_config(CONFIG_FORMAT, config_path)


def validate_urls(urls) -> bool:
    return not isinstance(urls, list) or not all(isinstance(url, str) for url in urls)


def get_feed_urls(config: Config) -> set[str]:
    urls = config.get("feed_urls", [])
    if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
        raise BrokenConfigError(f"feed_urls must be a list of strings: {urls}")
    return set(urls)


def set_feed_urls(config: Config, urls: set[str]) -> None:
    config["feed_urls"] = list(urls)
    if not isinstance(urls, set) or not all(isinstance(url, str) for url in urls):
        raise ValueError(f"feed_urls must be a set of strings: {urls}")
    set_config(config)


def add_feed_url(config: Config, url: str) -> None:
    feed_urls = get_feed_urls(config)
    feed_urls.add(url)
    set_feed_urls(config, feed_urls)


def delete_feed_url(config: Config, url: str) -> None:
    feed_urls = get_feed_urls(config)

    if url in feed_urls:
        feed_urls.remove(url)
        set_feed_urls(config, feed_urls)
    else:
        raise URLNotFoundError(f"URL {url} not found in feed_urls")


class URLNotFoundError(Exception):
    """Exception raised when a URL is not found in config feed URLs"""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class BrokenConfigError(Exception):
    """Exception raised when the config cannot be parsed."""

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message
        super().__init__(self.message)
