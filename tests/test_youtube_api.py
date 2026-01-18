import pytest

from data_miner.youtube_api import YouTubeAPI


@pytest.fixture
def yt():
    # New class doesn't take api_key; it accepts frontend data via set_data/extend_data
    return YouTubeAPI()


def test_set_data_replaces_internal_dataset(yt):
    data1 = [{"title": "Carrot prices today"}, {"title": "Potato market"}]
    data2 = [{"title": "Apple farming"}]

    yt.set_data(data1)
    assert yt.search_videos("carrot") == [data1[0]]

    yt.set_data(data2)
    assert yt.search_videos("carrot") == []
    assert yt.search_videos("apple") == [data2[0]]


def test_extend_data_appends(yt):
    data1 = [{"title": "Carrot prices today"}]
    data2 = [{"title": "Apple farming"}]

    yt.set_data(data1)
    yt.extend_data(data2)

    assert len(yt.search_videos("carrot")) == 1
    assert len(yt.search_videos("apple")) == 1


def test_set_data_validates_input_type(yt):
    with pytest.raises(TypeError):
        yt.set_data({"title": "not-a-list"})  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        yt.set_data([{"title": "ok"}, "bad"])  # type: ignore[list-item]


def test_search_videos_uses_internal_data_by_default(yt):
    dummy = [{"title": "Carrot price comparison"}, {"title": "Apple farming"}]
    yt.set_data(dummy)

    results = yt.search_videos("carrot")
    assert len(results) == 1
    assert "carrot" in results[0]["title"].lower()


def test_search_videos_can_search_passed_in_data_without_setting(yt):
    dummy = [{"title": "Carrot price comparison"}, {"title": "Apple farming"}]

    results = yt.search_videos("carrot", data=dummy)
    assert len(results) == 1
    assert "carrot" in results[0]["title"].lower()

    # internal data is still empty
    assert yt.search_videos("carrot") == []


def test_search_videos_matches_comments_primary_and_title_secondary(yt):
    dummy = [
        {"title": "Unrelated title", "comments": ["Carrots are cheaper at Costco"]},
        {"title": "Also unrelated", "comments": ["Nothing here"]},
        {"title": "Title mentions carrot", "comments": []},
    ]
    yt.set_data(dummy)

    results = yt.search_videos("carrot")

    # matches comment OR title, so should be 2 here
    assert len(results) == 2

    # Must include the comment match
    assert any(
        "costco" in " ".join(v.get("comments", [])).lower()
        for v in results
    )

    # And must include the title match
    assert any("title mentions carrot" in v.get("title", "").lower() for v in results)


def test_search_videos_case_insensitive(yt):
    dummy = [
        {"title": "X", "comments": ["CARROT prices are up"]},
        {"title": "Y", "comments": ["carrot prices are down"]},
    ]
    yt.set_data(dummy)

    results = yt.search_videos("CarRoT")
    assert len(results) == 2


def test_search_videos_handles_missing_comments(yt):
    dummy = [
        {"title": "Some title"},  # no comments key
        {"title": "Another", "comments": None},
        {"title": "Third", "comments": ["carrot mention"]},
    ]
    yt.set_data(dummy)

    results = yt.search_videos("carrot")
    assert len(results) == 1
    assert results[0]["title"] == "Third"


def test_search_videos_handles_comments_as_string_or_mixed_list(yt):
    dummy = [
        {"title": "A", "comments": "carrot is great"},                # str
        {"title": "B", "comments": [None, 123, "no match here"]},     # mixed
        {"title": "C", "comments": ["price", "CARROT deals"]},        # list[str]
    ]
    yt.set_data(dummy)

    results = yt.search_videos("carrot")
    assert {v["title"] for v in results} == {"A", "C"}


def test_search_videos_empty_query_returns_empty_list(yt):
    yt.set_data([{"title": "Carrot price comparison"}])

    assert yt.search_videos("") == []
    assert yt.search_videos("   ") == []
    assert yt.search_videos(None) == []  # type: ignore[arg-type]