"""Tests for load_songs (Phase 3 Step 1): the CSV comes back as dicts with real numbers."""
from pathlib import Path

import pytest

from src.recommender import NUMERIC_FIELDS, load_songs

# data/songs.csv relative to the repo root, resolved from this file so the path
# is right no matter which directory pytest is started from.
CSV_PATH = str(Path(__file__).resolve().parents[1] / "data" / "songs.csv")

REQUIRED_COLUMNS = (
    "id", "title", "artist", "genre", "mood",
    "energy", "tempo_bpm", "valence", "danceability", "acousticness",
)


def test_at_least_fifteen_songs():
    songs = load_songs(CSV_PATH)
    assert len(songs) >= 15


def test_numeric_fields_are_floats():
    for song in load_songs(CSV_PATH):
        for field in NUMERIC_FIELDS:
            assert isinstance(song[field], float), f"{song['title']}: {field} is {type(song[field]).__name__}"
        assert isinstance(song["id"], int), f"{song['title']}: id is {type(song['id']).__name__}"


def test_required_columns_present():
    for song in load_songs(CSV_PATH):
        for column in REQUIRED_COLUMNS:
            assert column in song, f"{song.get('title')} is missing column {column}"


def test_genres_are_diverse():
    genres = {song["genre"] for song in load_songs(CSV_PATH)}
    assert len(genres) >= 12


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_songs(str(Path(CSV_PATH).with_name("no_such_songs.csv")))
