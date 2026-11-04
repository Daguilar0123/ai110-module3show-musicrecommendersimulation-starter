"""Tests for the five extended song attributes (Challenge 1, agent mode, S7).

New columns: popularity, release_decade, mood_tags, explicit, duration_sec.
Scoring tests use hand-built songs, so they do not depend on the CSV; the two data tests read the real file.
"""
import csv
from pathlib import Path

import pytest

from src.recommender import load_songs, score_song

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "songs.csv"

NEW_COLUMNS = ("popularity", "release_decade", "mood_tags", "explicit", "duration_sec")
NEW_NUMERIC = ("popularity", "release_decade", "duration_sec")


def _base_song(**extra):
    """A song in the old ten-column shape (pop, happy); extra keys add the new attributes."""
    song = {
        "id": 1, "title": "Sunrise City", "artist": "Neon Echo", "genre": "pop", "mood": "happy",
        "energy": 0.82, "tempo_bpm": 118.0, "valence": 0.84, "danceability": 0.79, "acousticness": 0.18,
    }
    song.update(extra)
    return song


def _extended_song(**over):
    """A song carrying all five new keys, in the shape load_songs returns (numbers as floats)."""
    new = {"popularity": 100.0, "release_decade": 2010.0, "mood_tags": "nostalgic|warm",
           "explicit": "no", "duration_sec": 200.0}
    new.update(over)
    return _base_song(**new)


# --- data ---------------------------------------------------------------------------------------

def test_csv_has_five_new_columns():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)
    for column in NEW_COLUMNS:
        assert column in header, f"songs.csv has no {column} column"
    assert len(rows) >= 15
    for row in rows:
        title = row["title"]
        assert 0 <= int(row["popularity"]) <= 100, f"{title}: popularity out of range"
        assert int(row["release_decade"]) % 10 == 0, f"{title}: release_decade is not a decade"
        assert 2 <= len(row["mood_tags"].split("|")) <= 3, f"{title}: mood_tags needs 2-3 tags"
        assert row["explicit"] in ("yes", "no"), f"{title}: explicit must be yes/no"
        assert 120 <= int(row["duration_sec"]) <= 420, f"{title}: duration_sec out of range"


def test_new_numeric_columns_are_floats():
    for song in load_songs(str(CSV_PATH)):
        for field in NEW_NUMERIC:
            value = song.get(field)
            assert isinstance(value, float), f"{song['title']}: {field} is {type(value).__name__}"
        assert isinstance(song["mood_tags"], str) and isinstance(song["explicit"], str)


# --- scoring ------------------------------------------------------------------------------------

def test_popularity_adds_up_to_half_point():
    score, reasons = score_song({}, _extended_song(popularity=100.0))
    assert score == pytest.approx(0.5)
    assert "popular (+0.5)" in reasons

    score, reasons = score_song({}, _extended_song(popularity=82.0))
    assert score == pytest.approx(0.41)
    assert "popular (+0.41)" in reasons

    # Popularity 0 earns nothing, and says nothing.
    score, reasons = score_song({}, _extended_song(popularity=0.0))
    assert score == 0.0
    assert not any(r.startswith("popular") for r in reasons)


def test_decade_match_adds_half_point():
    song = _extended_song(popularity=0.0, release_decade=1990.0)   # popularity 0 isolates the decade term
    hit, hit_reasons = score_song({"favorite_decade": 1990}, song)
    assert hit == pytest.approx(0.5)
    assert "decade match (+0.5)" in hit_reasons

    miss, miss_reasons = score_song({"favorite_decade": 2010}, song)
    assert miss == 0.0
    assert not any("decade" in r for r in miss_reasons)

    none, _ = score_song({}, song)   # no favorite_decade in the profile: no term
    assert none == 0.0


def test_mood_tag_overlap_adds_half_point():
    song = _extended_song(popularity=0.0, mood_tags="nostalgic|warm")
    hit, reasons = score_song({"mood_tags": ["Warm", "dreamy"]}, song)   # one shared tag, case-insensitive
    assert hit == pytest.approx(0.5)   # one overlap earns the half point once, however many tags match
    assert "mood tag overlap (+0.5)" in reasons

    both, _ = score_song({"mood_tags": ["warm", "nostalgic"]}, song)
    assert both == pytest.approx(0.5)

    miss, miss_reasons = score_song({"mood_tags": ["angry"]}, song)
    assert miss == 0.0 and not any("mood tag" in r for r in miss_reasons)


def test_explicit_penalty_applies_only_when_asked():
    explicit = _extended_song(explicit="yes")
    clean = _extended_song(explicit="no")
    baseline, _ = score_song({}, explicit)

    penalised, reasons = score_song({"avoid_explicit": True}, explicit)
    assert penalised - baseline == pytest.approx(-1.0)
    assert "explicit (-1.0)" in reasons

    # Not asked (absent or False): no change and no reason.
    for prefs in ({}, {"avoid_explicit": False}):
        score, reasons = score_song(prefs, explicit)
        assert score == pytest.approx(baseline)
        assert not any(r.startswith("explicit") for r in reasons)

    # Asked, but the song is clean: no penalty.
    score, reasons = score_song({"avoid_explicit": True}, clean)
    assert score == pytest.approx(baseline)
    assert not any(r.startswith("explicit") for r in reasons)


def test_old_songs_without_new_keys_score_unchanged():
    old = _base_song()   # the ten original columns only
    plain = {"genre": "pop", "mood": "happy", "energy": 0.8}
    # Exact values from before this change: genre 2.0 + mood 1.0 + energy 0.98.
    assert score_song(plain, old) == (3.98, ["genre match (+2.0)", "mood match (+1.0)", "energy close to target (+0.98)"])
    # New-attribute prefs on a song with no new keys change nothing.
    extended_prefs = {**plain, "favorite_decade": 1990, "mood_tags": ["warm"], "avoid_explicit": True}
    assert score_song(extended_prefs, old) == score_song(plain, old)
    # And an empty profile still falls back to the no-match reason.
    assert score_song({}, old) == (0.0, ["no feature matched (+0.0)"])
