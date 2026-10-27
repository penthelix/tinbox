from typing import TypeVar

type Video = dict[str, str]

T = TypeVar("T")


class VideoFormat[T](dict[str, T | None]):
    """
    Represents a video format. Do not use this to represent actual fetched Video data.
    For that, use Video instead.
    """

    def __init__(
        self,
        title: T | None = None,
        description: T | None = None,
        link: T | None = None,
        published: T | None = None,
        val_type: type[T] = str,
    ) -> None:
        self.type = val_type
        for key in [title, description, link, published]:
            if not isinstance(key, self.type | None):
                raise TypeError(f"Key {key} is not of type {self.type | None}")
        super().__init__(
            title=title,
            description=description,
            link=link,
            published=published,
        )

    def to_string_dict(self) -> dict[str, str]:
        try:
            return {
                "title": str(self["title"]),
                "description": str(self["description"]),
                "link": str(self["link"]),
                "published": str(self["published"]),
            }
        except TypeError:
            raise TypeError("Cannot convert to string dict")
