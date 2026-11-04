import json
import platform
import subprocess
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path

from tinbox.defaults import CACHE_DATE_FORMAT, CACHE_VACCUUM_TIME
from tinbox.helper import sanitized_filename
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

get_cache_name: Callable[[str, datetime], str] = lambda channel_name, ts: (
    f"{ts.strftime(CACHE_DATE_FORMAT)}_{channel_name}_videos"
)
get_cache_name_now: Callable[[str], str] = lambda channel_name: get_cache_name(
    channel_name, datetime.now(UTC)
)
get_date_from_cache: Callable[[str], datetime] = lambda s: datetime.strptime(
    s[: s.find("_")], CACHE_DATE_FORMAT
).replace(tzinfo=UTC)
get_age_from_cache: Callable[[str], timedelta] = lambda s: (
    datetime.now(UTC) - get_date_from_cache(s)
)


def save_videos_to_cache(videos: list[Video], channel_name: str) -> bool:
    channel_name = sanitized_filename(channel_name)
    cache_fname: str = get_cache_name_now(channel_name)
    cache_path = CACHE_PATH / f"{cache_fname}.json"
    if not CACHE_PATH.exists():
        CACHE_PATH.mkdir(parents=True)
    with open(cache_path, "w") as f:
        json.dump(videos, f, indent=2)
    return True


def clear_cache() -> bool:
    _ = subprocess.run(["rm", "-rf", CACHE_PATH], check=True)
    return True


def prune_cache() -> bool:
    all_cache_files: list[Path] = [
        f for f in CACHE_PATH.glob("*.json") if (CACHE_PATH / f).is_file()
    ]
    all_cache_names: list[str] = [f.name for f in all_cache_files]
    all_cache_ages: list[timedelta] = list(map(get_age_from_cache, all_cache_names))
    all_caches: zip[tuple[Path, str, timedelta]] = zip(
        all_cache_files, all_cache_names, all_cache_ages
    )
    old_caches: filter[tuple[Path, str, timedelta]] = filter(
        lambda cache: cache[2] >= CACHE_VACCUUM_TIME, all_caches
    )
    old_cache_files: list[Path] = [cache[0] for cache in old_caches]
    _ = subprocess.run(["rm", *old_cache_files], check=True)
    return True
