import json
import os
import tempfile
import pytest

from data_miner.data_cleaner import DataCleaner


@pytest.fixture
def cleaner():
    return DataCleaner()


def test_load_json(cleaner):
    sample = [{"a": 1}, {"b": 2}]

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
        json.dump(sample, f)
        path = f.name

    try:
        data = cleaner.load_json(path)
        assert data == sample
    finally:
        os.remove(path)


def test_remove_nulls(cleaner):
    records = [{"a": 1, "b": None}, {"c": 2, "d": None}]
    assert cleaner.remove_nulls(records) == [{"a": 1}, {"c": 2}]


def test_normalize_text(cleaner):
    assert cleaner.normalize_text("  Hello World ") == "hello world"


def test_clean_youtube_data(cleaner):
    raw = [{
        "title": "  Test Video ",
        "channel": "MyChannel",
        "views": "10",
        "published_at": "2024-01-01",
    }]

    cleaned = cleaner.clean_youtube_data(raw)

    assert cleaned[0]["title"] == "test video"
    assert cleaned[0]["channel"] == "mychannel"
    assert cleaned[0]["views"] == 10
    assert cleaned[0]["published_at"] == "2024-01-01"

def test_clean_youtube_data_includes_comments_and_normalizes(cleaner):
    raw = [
        {
            "title": "  Test Video ",
            "channel": "MyChannel",
            "views": "10",
            "published_at": "2024-01-01",
            "comments": ["  Great VIDEO  ", "Price of carrots is HIGH ", None, ""],
        }
    ]

    cleaned = cleaner.clean_youtube_data(raw)

    assert cleaned == [
        {
            "title": "test video",
            "channel": "mychannel",
            "views": 10,
            "published_at": "2024-01-01",
            "comments": ["great video", "price of carrots is high"],
        }
    ]

def test_clean_youtube_data_comments_missing_defaults_to_empty_list(cleaner):
    raw = [{"title": "Video", "channel": "Chan", "views": "5"}]
    cleaned = cleaner.clean_youtube_data(raw)

    assert cleaned[0]["comments"] == []


def test_clean_youtube_data_comments_string_is_wrapped_into_list(cleaner):
    raw = [{"title": "Video", "channel": "Chan", "views": "5", "comments": "  Hello  "}]
    cleaned = cleaner.clean_youtube_data(raw)

    assert cleaned[0]["comments"] == ["hello"]


@pytest.mark.parametrize("views_value", [None, "not-a-number", "10,000", "", []])
def test_clean_youtube_data_bad_views_does_not_crash(cleaner, views_value):
    raw = [{"title": "Video", "channel": "Chan", "views": views_value, "comments": []}]
    cleaned = cleaner.clean_youtube_data(raw)

    # Expect fallback to 0 (assuming you used safe int parsing)
    assert cleaned[0]["views"] == 0