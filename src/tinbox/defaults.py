from datetime import timedelta

from tinbox.types import VideoFormat

CACHE_VACCUUM_TIME: timedelta = timedelta(days=30)
CACHE_DATE_FORMAT: str = "%Y-%m-%d-%H-%M-%S"

TABLE_COLORS = VideoFormat(
    title="#ffffff",
    description="#ffffff",
    link="#ffffff",
    published="#ffffff",
)

TABLE_COLS = VideoFormat(
    title=50,
    description=20,
    link=20,
    published=40,
    val_type=int,
)

MANDATORY_FIELDS = VideoFormat(
    title=True,
    description=False,
    link=True,
    published=False,
    val_type=bool,
)
