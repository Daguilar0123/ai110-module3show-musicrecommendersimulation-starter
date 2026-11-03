"""Tests for the artist diversity penalty (Challenge 3)."""
import copy

from src.diversity import apply_artist_penalty
from src.recommender import load_songs, recommend_songs


def _song(title, artist):
    return {"title": title, "artist": artist}


def _scored():
    return [
        (_song("A1", "A"), 3.0, ["genre match (+2.0)"]),
        (_song("A2", "A"), 2.9, ["mood match (+1.0)"]),
        (_song("B1", "B"), 2.8, ["genre match (+2.0)"]),
    ]


def test_second_song_by_same_artist_is_penalized():
    result = apply_artist_penalty(_scored(), penalty=0.5)
    assert [s["title"] for s, _, _ in result] == ["A1", "B1", "A2"]
    assert result[2][1] == 2.4   # 2.9 - 0.5


def test_penalty_adds_a_reason():
    result = apply_artist_penalty(_scored(), penalty=0.5)
    by_title = {s["title"]: reasons for s, _, reasons in result}
    assert "artist already listed (-0.50)" in by_title["A2"]
    assert not any("artist already listed" in r for r in by_title["A1"])
    assert not any("artist already listed" in r for r in by_title["B1"])


def test_zero_penalty_is_identity():
    scored = _scored()
    assert apply_artist_penalty(scored, penalty=0) == scored


def test_input_not_mutated():
    scored = _scored()
    snapshot = copy.deepcopy(scored)
    apply_artist_penalty(scored, penalty=0.5)
    assert scored == snapshot


def test_recommend_songs_with_penalty_changes_top_list():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "edm", "mood": "euphoric", "energy": 0.9}   # Neon Echo has three songs and two reach the top 5
    plain = recommend_songs(prefs, songs, k=5)
    penalized = recommend_songs(prefs, songs, k=5, diversity_penalty=1.0)
    count = lambda results: sum(1 for s, _, _ in results if s["artist"] == "Neon Echo")   # noqa: E731
    assert count(plain) == 2   # guards the setup: without this the test could pass for the wrong reason
    assert count(penalized) <= 1
    assert [s["id"] for s, _, _ in plain] != [s["id"] for s, _, _ in penalized]
