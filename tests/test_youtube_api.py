# --------------------------------------------------
# tests/test_youtube_api.py

import tempfile
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from data_miner.youtube_api import YouTubeAPI


def test_load_dummy_data():
    yt = YouTubeAPI()

    sample = [
        {"title": "Carrot prices today"},
        {"title": "Potato market"}
    ]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump(sample, f)
        path = f.name

    data = yt.load_dummy_data(path)
    assert data == sample


def test_search_videos(monkeypatch):
    yt = YouTubeAPI()

    dummy = [
        {"title": "Carrot price comparison"},
        {"title": "Apple farming"}
    ]

    def mock_loader(path):
        return dummy

    monkeypatch.setattr(yt, "load_dummy_data", mock_loader)

    results = yt.search_videos("carrot")

    assert len(results) == 1
    assert "carrot" in results[0]["title"].lower()


monkeypatch.setattr(yt, "load_dummy_data", mock_loader)


results = yt.search_videos("carrot")


assert len(results) == 1
assert "carrot" in results[0]["title"].lower()
