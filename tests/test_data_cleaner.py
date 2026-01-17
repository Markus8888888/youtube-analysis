# --------------------------------------------------
# tests/test_data_cleaner.py

import tempfile
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from data_miner.data_cleaner import DataCleaner

def test_load_json():
    cleaner = DataCleaner()
    sample = [{"a": 1}, {"b": 2}]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump(sample, f)
        path = f.name

    data = cleaner.load_json(path)
    assert data == sample


def test_remove_nulls():
    cleaner = DataCleaner()

    records = [
        {"a": 1, "b": None},
        {"c": 2, "d": None}
    ]

    cleaned = cleaner.remove_nulls(records)

    assert cleaned == [{"a": 1}, {"c": 2}]


def test_normalize_text():
    cleaner = DataCleaner()
    assert cleaner.normalize_text("  Hello World ") == "hello world"


def test_clean_youtube_data():
    cleaner = DataCleaner()

    raw = [
        {
            "title": "  Test Video ",
            "channel": "MyChannel",
            "views": "10",
            "published_at": "2024-01-01"
        }
    ]

    cleaned = cleaner.clean_youtube_data(raw)

    assert cleaned[0]["title"] == "test video"
    assert cleaned[0]["channel"] == "mychannel"
    assert cleaned[0]["views"] == 10
