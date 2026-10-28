from tinbox.types import VideoFormat

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
