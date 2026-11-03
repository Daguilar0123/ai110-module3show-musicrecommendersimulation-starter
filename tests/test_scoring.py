"""Tests for score_song, recommend_songs and the OOP bridge (S3, Phase 3 Steps 2, 3 and 5).

Songs are built by hand in the same shape load_songs returns (CSV header, numeric fields as floats),
so these tests do not depend on load_songs.
"""
from functools import partial

import pytest

from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    profile_to_prefs,
    recommend_songs,
    score_song,
)


def _song(id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness):
    return {
        "id": id, "title": title, "artist": artist, "genre": genre, "mood": mood,
        "energy": energy, "tempo_bpm": tempo_bpm, "valence": valence,
        "danceability": danceability, "acousticness": acousticness,
    }


@pytest.fixture
def songs():
    """Six rows copied from data/songs.csv: two pop, one indie pop, one lofi, one rock, one sad pop."""
    return [
        _song(1, "Sunrise City", "Neon Echo", "pop", "happy", 0.82, 118.0, 0.84, 0.79, 0.18),
        _song(2, "Midnight Coding", "LoRoom", "lofi", "chill", 0.42, 78.0, 0.56, 0.62, 0.71),
        _song(3, "Storm Runner", "Voltline", "rock", "intense", 0.91, 152.0, 0.48, 0.66, 0.10),
        _song(5, "Gym Hero", "Max Pulse", "pop", "intense", 0.93, 132.0, 0.77, 0.88, 0.05),
        _song(10, "Rooftop Lights", "Indigo Parade", "indie pop", "happy", 0.76, 124.0, 0.81, 0.82, 0.35),
        _song(19, "Rain on the Radio", "June Alder", "pop", "sad", 0.55, 76.0, 0.25, 0.50, 0.45),
    ]


def _by_id(songs, song_id):
    return next(s for s in songs if s["id"] == song_id)


def test_genre_match_adds_two_points(songs):
    prefs = {"genre": "pop"}
    pop_score, _ = score_song(prefs, _by_id(songs, 1))
    rock_score, _ = score_song(prefs, _by_id(songs, 3))
    assert pop_score == pytest.approx(2.0)
    assert pop_score - rock_score == pytest.approx(2.0)


def test_partial_genre_match_adds_half(songs):
    indie_pop = _by_id(songs, 10)
    pop = _by_id(songs, 1)

    # "pop" inside "indie pop": half of the genre weight, and the reason says so.
    score, reasons = score_song({"genre": "pop"}, indie_pop)
    assert score == pytest.approx(1.0)
    assert "genre partial match (+1.0)" in reasons

    # Containment works in the other direction too, and is case-insensitive.
    score, _ = score_song({"genre": "Indie Pop"}, pop)
    assert score == pytest.approx(1.0)

    # An exact match is worth strictly more than a partial one.
    exact, _ = score_song({"genre": "pop"}, pop)
    assert exact > 1.0


def test_mood_match_adds_one_point(songs):
    prefs = {"mood": "happy"}
    happy_score, reasons = score_song(prefs, _by_id(songs, 1))
    chill_score, _ = score_song(prefs, _by_id(songs, 2))
    assert happy_score == pytest.approx(1.0)
    assert chill_score == pytest.approx(0.0)
    assert "mood match (+1.0)" in reasons


def test_valence_term_only_when_profile_has_target(songs):
    song = _by_id(songs, 1)  # valence 0.84
    without = score_song({"genre": "pop"}, song)
    with_target = score_song({"genre": "pop", "valence": 0.8}, song)

    # No valence in the profile: no points and no reason.
    assert not any("valence" in r for r in without[1])
    # With a target: 0.5 * (1 - |0.84 - 0.8|) = 0.48 extra, named in the reasons.
    assert with_target[0] - without[0] == pytest.approx(0.48)
    assert "valence close to target (+0.48)" in with_target[1]


def test_energy_similarity_rewards_closeness(songs):
    song = _by_id(songs, 1)  # energy 0.82
    near, near_reasons = score_song({"energy": 0.8}, song)
    far, _ = score_song({"energy": 0.2}, song)
    assert near == pytest.approx(0.98)
    assert far == pytest.approx(0.38)
    assert near > far
    assert "energy close to target (+0.98)" in near_reasons


def test_every_song_gets_a_float_score(songs):
    full = {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8, "likes_acoustic": False}
    for prefs in (full, {}):  # a complete profile, and one that matches nothing at all
        for song in songs:
            score, reasons = score_song(prefs, song)
            assert isinstance(score, float)
            assert reasons, "reasons must never be empty"
    assert score_song({}, songs[0]) == (0.0, ["no feature matched (+0.0)"])


def test_reasons_name_the_feature_and_points(songs):
    _, reasons = score_song({"genre": "pop", "mood": "happy", "energy": 0.8}, _by_id(songs, 1))
    assert "genre match (+2.0)" in reasons
    assert "mood match (+1.0)" in reasons


def test_recommend_songs_sorted_descending(songs):
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8}
    results = recommend_songs(prefs, songs, k=len(songs))
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)
    song, score, explanation = results[0]
    assert song["title"] == "Sunrise City"
    assert isinstance(explanation, str) and "genre match (+2.0)" in explanation


def test_recommend_songs_returns_k(songs):
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    assert len(recommend_songs(prefs, songs, k=3)) == 3
    assert len(recommend_songs(prefs, songs)) == 5  # default k
    assert len(recommend_songs(prefs, songs, k=100)) == len(songs)  # never more than the catalog


def test_custom_weights_change_ranking(songs):
    prefs = {"genre": "lofi", "energy": 0.9}
    default_top = recommend_songs(prefs, songs, k=1)[0][0]
    # A partial dict: genre and energy only, the rest fill in from DEFAULT_WEIGHTS.
    energy_scorer = partial(score_song, weights={"genre": 0.0, "energy": 3.0})
    custom_top = recommend_songs(prefs, songs, k=1, scorer=energy_scorer)[0][0]
    assert default_top["title"] == "Midnight Coding"  # the lofi song wins on genre
    assert custom_top["title"] == "Storm Runner"      # energy 0.91 is closest to 0.9
    assert default_top["id"] != custom_top["id"]


def test_recommender_class_delegates(songs):
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    song_objects = [Song(**s) for s in songs]
    results = Recommender(song_objects).recommend(user, k=4)

    expected = recommend_songs(profile_to_prefs(user), songs, k=4)
    assert all(isinstance(s, Song) for s in results)
    assert [s.id for s in results] == [s["id"] for s, _, _ in expected]
    assert results[0] is song_objects[0]  # the original Song object, not a copy


def test_close_far_label_follows_closeness_not_weighted_points(songs):
    song = _by_id(songs, 1)  # energy 0.82, valence 0.84
    # Gap 0.70 -> closeness 0.30, which is "far" however much the energy weight is raised.
    _, light = score_song({"energy": 0.12}, song, {"energy": 1.0})
    _, heavy = score_song({"energy": 0.12}, song, {"energy": 2.0})
    assert "energy far from target (+0.30)" in light
    assert "energy far from target (+0.60)" in heavy  # +0.60 is >= 0.5 points, but still "far"
    # A close energy stays "close" at either weight; the points in parentheses are weight x closeness.
    _, close_heavy = score_song({"energy": 0.8}, song, {"energy": 2.0})
    assert "energy close to target (+1.96)" in close_heavy
    # Valence gets the same close/far word: gap 0.64 -> closeness 0.36 -> far.
    _, far_valence = score_song({"valence": 0.2}, song)
    assert "valence far from target (+0.18)" in far_valence


def test_zero_weight_term_leaves_its_reason_out(songs):
    song = _by_id(songs, 1)
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8, "likes_acoustic": False}
    # Zero only the mood weight: its reason goes, the other reasons stay.
    _, reasons = score_song(prefs, song, {"mood": 0.0})
    assert not any(r.startswith("mood") for r in reasons)
    assert "genre match (+2.0)" in reasons
    # Zero every weight: nothing is left to say, so the fallback reason appears.
    all_zero = {k: 0.0 for k in ("genre", "mood", "energy", "valence", "acoustic")}
    assert score_song(prefs, song, all_zero) == (0.0, ["no feature matched (+0.0)"])


def test_mood_match_is_case_insensitive(songs):
    score, reasons = score_song({"mood": " Happy "}, _by_id(songs, 1))  # song mood is "happy"
    assert score == pytest.approx(1.0)
    assert "mood match (+1.0)" in reasons


def test_different_profiles_give_different_tops(songs):
    pop_happy = {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8}
    intense_rock = {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.45}
    pop_top = recommend_songs(pop_happy, songs, k=1)[0][0]
    rock_top = recommend_songs(intense_rock, songs, k=1)[0][0]
    assert pop_top["title"] == "Sunrise City"
    assert rock_top["title"] == "Storm Runner"
    assert pop_top["id"] != rock_top["id"]
