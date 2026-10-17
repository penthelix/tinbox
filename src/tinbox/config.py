import configparser
from pathlib import Path

CONFIG_PATH: Path = Path.home() / ".config" / "tinbox" / "config.ini"
config = configparser.ConfigParser()


def init_config() -> None:
    global config
    config = configparser.ConfigParser()
    save_config()


def add_feed(feed_name: str, feed_url: str) -> None:
    config[f"feeds.{feed_name}"] = {"url": feed_url}
    save_config()


def remove_feed(feed_name: str) -> None:
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


def save_config() -> None:
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)
