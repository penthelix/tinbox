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


def set_attribute(key: str, value: str) -> None:
    config = get_config()
    config[key] = value
    set_config(config)


def get_attribute(key: str) -> str:
    config = get_config()
    return config[key]


def get_feed_urls() -> set[str]:
    return set(get_attribute("feed_urls"))
