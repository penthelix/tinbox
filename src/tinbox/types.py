from collections.abc import Callable
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
        super().__init__(
            title=title,
            description=description,
            link=link,
            published=published,
        )
        self.validate_values(attempt_type_conversion=True)

    def _type_to_fn(self) -> Callable:
        if self.type == str:
            return lambda x: str(x)
        if self.type == int:
            return lambda x: int(x)
        if self.type == float:
            return lambda x: float(x)
        if self.type == bool:
            return lambda x: bool(x)
        return lambda x: x

    def validate_values(self, attempt_type_conversion: bool = False) -> None:
        is_correct_type = lambda value: isinstance(value, self.type | None)
        if attempt_type_conversion:
            for key, value in self.items():
                if not is_correct_type(value):
                    self[key] = self._type_to_fn()(value)
        for value in self.values():
            if not is_correct_type(value):
                raise TypeError(f"Value {value} is not of type {self.type | None}")

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
