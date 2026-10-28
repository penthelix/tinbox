import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path

from tinbox.types import Video

CACHE_PATH = Path()
match platform.system():
    case "Windows":
        CACHE_PATH = Path.home() / "AppData" / "Local" / "tinbox"
    case "Linux":
        CACHE_PATH = Path.home() / ".cache" / "tinbox"
    case "Darwin":
        CACHE_PATH = Path.home() / "Library" / "Caches" / "tinbox"
    case _:
        raise NotImplementedError(f"Unsupported platform: {platform.system()}")


def save_videos_to_cache(videos: list[Video], channel_name: str) -> bool:
    cache_fname: str = (
        f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{channel_name}_videos"
    )
    cache_path = CACHE_PATH / f"{cache_fname}.json"
    with open(cache_path, "w") as f:
        json.dump(videos, f, indent=2)
    return True


def clear_cache() -> bool:
    _ = subprocess.run(["rm", "-rf", CACHE_PATH], check=True)
    return True
