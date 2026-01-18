import pytest

from data_miner.youtube_link_processor import YouTubeLinkProcessor
from data_miner.youtube_data_processor import YouTubeDataProcessor
from data_miner.youtube_api import YouTubeAPI

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def data_processor():
    return YouTubeDataProcessor()


@pytest.fixture
def link_processor(monkeypatch):
    # Link processor requires an API key; set a dummy key via env
    monkeypatch.setenv("YOUTUBE_API_KEY", "fake-test-key")
    return YouTubeLinkProcessor()


# -----------------------------
# YouTubeDataProcessor tests
# -----------------------------
def test_set_data_replaces_internal_dataset(data_processor):
    data1 = [{"title": "Carrot prices today"}, {"title": "Potato market"}]
    data2 = [{"title": "Apple farming"}]

    data_processor.set_data(data1)
    assert data_processor.search_videos("carrot") == [data1[0]]

    data_processor.set_data(data2)
    assert data_processor.search_videos("carrot") == []
    assert data_processor.search_videos("apple") == [data2[0]]


def test_extend_data_appends(data_processor):
    data1 = [{"title": "Carrot prices today"}]
    data2 = [{"title": "Apple farming"}]

    data_processor.set_data(data1)
    data_processor.extend_data(data2)

    assert len(data_processor.search_videos("carrot")) == 1
    assert len(data_processor.search_videos("apple")) == 1


def test_set_data_validates_input_type(data_processor):
    with pytest.raises(TypeError):
        data_processor.set_data({"title": "not-a-list"})  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        data_processor.set_data([{"title": "ok"}, "bad"])  # type: ignore[list-item]


def test_search_videos_uses_internal_data_by_default(data_processor):
    dummy = [{"title": "Carrot price comparison"}, {"title": "Apple farming"}]
    data_processor.set_data(dummy)

    results = data_processor.search_videos("carrot")
    assert len(results) == 1
    assert "carrot" in results[0]["title"].lower()


def test_search_videos_can_search_passed_in_data_without_setting(data_processor):
    dummy = [{"title": "Carrot price comparison"}, {"title": "Apple farming"}]

    results = data_processor.search_videos("carrot", data=dummy)
    assert len(results) == 1
    assert "carrot" in results[0]["title"].lower()

    # internal data is still empty
    assert data_processor.search_videos("carrot") == []


def test_search_videos_matches_comments_primary_and_title_secondary(data_processor):
    dummy = [
        {"title": "Unrelated title", "comments": ["Carrots are cheaper at Costco"]},
        {"title": "Also unrelated", "comments": ["Nothing here"]},
        {"title": "Title mentions carrot", "comments": []},
    ]
    data_processor.set_data(dummy)

    results = data_processor.search_videos("carrot")

    # matches comment OR title, so should be 2 here
    assert len(results) == 2

    # Must include the comment match
    assert any(
        "costco" in " ".join(v.get("comments", [])).lower()
        for v in results
    )

    # And must include the title match
    assert any("title mentions carrot" in v.get("title", "").lower() for v in results)


def test_search_videos_case_insensitive(data_processor):
    dummy = [
        {"title": "X", "comments": ["CARROT prices are up"]},
        {"title": "Y", "comments": ["carrot prices are down"]},
    ]
    data_processor.set_data(dummy)

    results = data_processor.search_videos("CarRoT")
    assert len(results) == 2


def test_search_videos_handles_missing_comments(data_processor):
    dummy = [
        {"title": "Some title"},  # no comments key
        {"title": "Another", "comments": None},
        {"title": "Third", "comments": ["carrot mention"]},
    ]
    data_processor.set_data(dummy)

    results = data_processor.search_videos("carrot")
    assert len(results) == 1
    assert results[0]["title"] == "Third"


def test_search_videos_handles_comments_as_string_or_mixed_list(data_processor):
    dummy = [
        {"title": "A", "comments": "carrot is great"},                # str
        {"title": "B", "comments": [None, 123, "no match here"]},     # mixed
        {"title": "C", "comments": ["price", "CARROT deals"]},        # list[str]
    ]
    data_processor.set_data(dummy)

    results = data_processor.search_videos("carrot")
    assert {v["title"] for v in results} == {"A", "C"}


def test_search_videos_empty_query_returns_empty_list(data_processor):
    data_processor.set_data([{"title": "Carrot price comparison"}])

    assert data_processor.search_videos("") == []
    assert data_processor.search_videos("   ") == []
    assert data_processor.search_videos(None) == []  # type: ignore[arg-type]


# -----------------------------
# YouTubeLinkProcessor tests (no network)
# -----------------------------
@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=abc123XYZ", "abc123XYZ"),
        ("https://youtu.be/abc123XYZ", "abc123XYZ"),
        ("https://www.youtube.com/shorts/abc123XYZ", "abc123XYZ"),
        ("https://www.youtube.com/embed/abc123XYZ", "abc123XYZ"),
        ("https://www.youtube.com/watch?v=abc123XYZ&t=10s", "abc123XYZ"),
    ],
)
def test_extract_video_id(link_processor, url, expected):
    assert link_processor.extract_video_id(url) == expected


def test_extract_video_id_invalid_returns_none(link_processor):
    assert link_processor.extract_video_id("") is None
    assert link_processor.extract_video_id("not a url") is None
    assert link_processor.extract_video_id("https://example.com/watch?v=abc") is None
