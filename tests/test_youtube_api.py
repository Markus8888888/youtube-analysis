import json
import os
import tempfile
import pytest

from data_miner.youtube_api import YouTubeAPI


@pytest.fixture
def yt():
    return YouTubeAPI(api_key=None)


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
