import configparser
from pathlib import Path
from typing import cast

from tinbox.defaults import TABLE_COLORS
from tinbox.helper import is_hex_code
from tinbox.types import VideoFormat

CONFIG_PATH: Path = Path.home() / ".config" / "tinbox" / "config.ini"
config = configparser.ConfigParser()


def init_config() -> None:
    global config
    config = configparser.ConfigParser()
    config["DEFAULT.tableColors"] = TABLE_COLORS
    save_config()


def add_feed(feed_name: str, feed_url: str) -> None:
    config[f"feeds.{feed_name}"] = {"url": feed_url}
    save_config()


def remove_feed(feed_name: str | None = None, feed_url: str | None = None) -> None:
    if feed_name and feed_url:
        raise ValueError("Only one of feed_name or feed_url can be provided")

    if not feed_name and not feed_url:
        raise ValueError("Either feed_name or feed_url must be provided")

    if feed_url:
        feed_name = next(
            (
                key.replace("feeds.", "")
                for key in config.sections()
                if config[key]["url"] == feed_url
            ),
            None,
        )

    if not feed_name:
        raise FeedURLNotFoundError(f"Feed with URL {feed_url} not found")

    config.remove_section(f"feeds.{feed_name}")
    save_config()


def list_feed_names() -> set[str]:
    _ = config.read(CONFIG_PATH)
    return {
        key.replace("feeds.", "")
        for key in config.sections()
        if key.startswith("feeds.")
    }


def list_feed_urls() -> set[str]:
    _ = config.read(CONFIG_PATH)
    return {config[key]["url"] for key in config.sections() if key.startswith("feeds.")}


def get_table_colors() -> VideoFormat:
    try:
        colors = cast(VideoFormat, config["DEFAULT.tableColors"])
    except KeyError:
        config["DEFAULT.tableColors"] = TABLE_COLORS
        colors = TABLE_COLORS
    for code in colors.values():
        if not is_hex_code(code):
            raise BrokenConfigError(f"Invalid color code: {code}")
    return colors


def save_config() -> None:
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)


class FeedURLNotFoundError(Exception):
    """Exception raised when a feed URL is not found."""

    def init__(self, feed_url: str) -> None:
        super().__init__(f"Feed {feed_url} not found")


class BrokenConfigError(Exception):
    """Exception raised when the config file is broken."""

    def init__(self, message: str) -> None:
        super().__init__(f"Config file is broken: {message}")
