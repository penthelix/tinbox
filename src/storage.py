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
