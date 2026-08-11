from pathlib import Path

import pytest

from src.tinbox.config import (
    CONFIG_FORMAT,
    CONFIG_PATH,
    # add_feed_url,
    # delete_feed_url,
    get_config,
    set_config,
)


def test_main():
    assert isinstance(CONFIG_PATH, Path)
    assert isinstance(CONFIG_FORMAT, dict)
    assert isinstance(CONFIG_FORMAT["feed_urls"], list)


def test_get_config():
    returned_config = get_config()
    assert isinstance(returned_config, dict)

    format_keys = CONFIG_FORMAT.keys()
    returned_keys = returned_config.keys()
    assert format_keys == returned_keys

    for key in format_keys:
        assert isinstance(returned_config[key], type(CONFIG_FORMAT[key])), (
            f"Returned config has incorrect type for key: {key}"
        )

    file_path_that_definitely_does_not_exist: Path = Path(
        "this/path/does/not/exist.json"
    )
    with pytest.raises(FileNotFoundError):
        get_config(file_path_that_definitely_does_not_exist)


def test_set_config():
    test_config_path = "tests/test_config.json"
    returned_val = set_config({"test_key": "test_value"}, test_config_path)
    assert returned_val is None
    assert get_config(test_config_path) == {"test_key": "test_value"}


# def test_add_feed_url():
#     add_feed_url("https://example.com/feed.xml")
#     assert "https://example.com/feed.xml" in CONFIG_FORMAT["feeds"]
#     delete_feed_url("https://example.com/feed.xml")


# def test_delete_feed_url():
#     add_feed_url("https://example.com/feed.xml")
#     delete_feed_url("https://example.com/feed.xml")
#     assert "https://example.com/feed.xml" not in CONFIG_FORMAT["feeds"]
