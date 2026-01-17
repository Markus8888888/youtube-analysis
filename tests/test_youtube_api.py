import json
import os
import tempfile
import pytest

from data_miner.youtube_api import YouTubeAPI


@pytest.fixture
def yt():
    return YouTubeAPI(api_key="fake-test-key")


def test_load_dummy_data(yt):
    sample = [{"title": "Carrot prices today"}, {"title": "Potato market"}]

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
        json.dump(sample, f)
        path = f.name

    try:
        assert yt.load_dummy_data(path) == sample
    finally:
        os.remove(path)


def test_search_videos(monkeypatch):
    yt = YouTubeAPI()
    dummy = [{"title": "Carrot price comparison"}, {"title": "Apple farming"}]

    monkeypatch.setattr(yt, "load_dummy_data", lambda _path: dummy)

    results = yt.search_videos("carrot")
    assert len(results) == 1
    assert "carrot" in results[0]["title"].lower()

def test_load_dummy_data_reads_json_file(yt):
    sample = [{"title": "A", "comments": ["x"]}, {"title": "B", "comments": []}]

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
        json.dump(sample, f)
        path = f.name

    try:
        assert yt.load_dummy_data(path) == sample
    finally:
        os.remove(path)


def test_search_videos_matches_comments_primary(monkeypatch):
    yt = YouTubeAPI(api_key="fake-test-key")

    dummy = [
        {"title": "Unrelated title", "comments": ["Carrots are cheaper at Costco"]},
        {"title": "Also unrelated", "comments": ["Nothing here"]},
        {"title": "Title mentions carrot", "comments": []},
    ]

    monkeypatch.setattr(yt, "load_dummy_data", lambda _path: dummy)

    results = yt.search_videos("carrot")

    # If your implementation matches comments OR title:
    assert len(results) in (1, 2)

    # Must at least include the comment match
    assert any(
        "costco" in " ".join(v.get("comments", [])).lower()
        for v in results
    )


def test_search_videos_case_insensitive(monkeypatch):
    yt = YouTubeAPI(api_key="fake-test-key")

    dummy = [
        {"title": "X", "comments": ["CARROT prices are up"]},
        {"title": "Y", "comments": ["carrot prices are down"]},
    ]
    monkeypatch.setattr(yt, "load_dummy_data", lambda _path: dummy)

    results = yt.search_videos("CarRoT")
    assert len(results) == 2


def test_search_videos_handles_missing_comments(monkeypatch):
    yt = YouTubeAPI(api_key="fake-test-key")

    dummy = [
        {"title": "Some title"},  # no comments key
        {"title": "Another", "comments": None},
        {"title": "Third", "comments": ["carrot mention"]},
    ]
    monkeypatch.setattr(yt, "load_dummy_data", lambda _path: dummy)

    results = yt.search_videos("carrot")
    assert len(results) == 1
    assert results[0]["title"] == "Third"