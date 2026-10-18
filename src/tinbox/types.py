type Video = dict[str, str]


class VideoFormat(dict):
    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        link: str | None = None,
        published: str | None = None,
    ) -> None:
        super().__init__(
            title=title,
            description=description,
            link=link,
            published=published,
        )
