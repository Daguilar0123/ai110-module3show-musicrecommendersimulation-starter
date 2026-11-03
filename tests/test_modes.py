"""Tests for the Strategy ranking modes (Challenge 2)."""
import pytest

from src.ranking_modes import MODES, get_scorer
from src.recommender import recommend_songs, score_song


def make_song(song_id, title, genre, mood, energy):
    return {"id": song_id, "title": title, "artist": f"Artist {song_id}", "genre": genre, "mood": mood,
            "energy": energy, "tempo_bpm": 100.0, "valence": 0.5, "danceability": 0.5, "acousticness": 0.5}


def test_each_mode_returns_callable():
    for mode in MODES:
        assert callable(get_scorer(mode))


def test_unknown_mode_raises():
    with pytest.raises(ValueError) as excinfo:
        get_scorer("nonsense")
    for mode in MODES:   # the message lists the valid modes
        assert mode in str(excinfo.value)


def test_weighted_is_score_song_itself():
    assert get_scorer("weighted") is score_song


def test_genre_first_outranks_weighted_on_genre():
    prefs = {"genre": "rock", "energy": 0.9}
    genre_match = make_song(1, "Genre Match", "rock", "calm", 0.3)    # right genre, energy far off
    energy_match = make_song(2, "Energy Match", "pop", "calm", 0.9)   # wrong genre, energy exact
    gf, em = get_scorer("genre_first"), get_scorer("energy_similarity")
    assert gf(prefs, genre_match)[0] > gf(prefs, energy_match)[0]
    assert em(prefs, genre_match)[0] < em(prefs, energy_match)[0]


def test_modes_plug_into_recommend_songs():
    prefs = {"genre": "pop", "mood": "happy"}
    mood_match = make_song(1, "Mood Match", "rock", "happy", 0.5)
    genre_match = make_song(2, "Genre Match", "pop", "sad", 0.5)
    results = recommend_songs(prefs, [genre_match, mood_match], k=2, scorer=get_scorer("mood_first"))
    assert results[0][0]["title"] == "Mood Match"


def test_explicit_weights_override_mode_weights():
    prefs = {"genre": "rock"}
    song = make_song(1, "S", "rock", "calm", 0.5)
    score, _ = get_scorer("genre_first")(prefs, song, {"genre": 1.0})
    assert score == 1.0
