"""Music Recommender Simulation: core logic (CLI-first)."""
from __future__ import annotations
import csv
from dataclasses import asdict, dataclass
from typing import Callable, Dict, List, Optional, Tuple

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


NUMERIC_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")   # S2 converts these to float; "id" to int
DEFAULT_WEIGHTS: Dict[str, float] = {"genre": 2.0, "mood": 1.0, "energy": 1.0, "valence": 0.5, "acoustic": 0.5}   # decided Nov 2, 2026: partial genre match = half points; valence only when the profile has a target

Scorer = Callable[[Dict, Dict, Optional[Dict]], Tuple[float, List[str]]]


def load_songs(csv_path: str) -> List[Dict]:
    """Read the CSV into a list of dicts; NUMERIC_FIELDS become floats, id becomes int."""
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            songs = list(csv.DictReader(f))
    except FileNotFoundError:
        raise FileNotFoundError(f"Song catalog not found at '{csv_path}'. Check the path to songs.csv.") from None
    for song in songs:
        song["id"] = int(song["id"])
        for field in NUMERIC_FIELDS:
            song[field] = float(song[field])
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Score one song against user_prefs; returns (score, reasons) using weights or DEFAULT_WEIGHTS."""
    raise NotImplementedError  # S3 (S7 extends the body for new columns)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    scorer: Optional[Scorer] = None, diversity_penalty: float = 0.0) -> List[Tuple[Dict, float, str]]:
    """Score every song with scorer (default score_song), apply the artist penalty if > 0, return the top k as (song, score, explanation)."""
    raise NotImplementedError  # S3


def profile_to_prefs(user: UserProfile) -> Dict:
    """Bridge the OOP profile to the functional dict: genre, mood, energy, likes_acoustic."""
    raise NotImplementedError  # S3


class Recommender:
    """OOP wrapper required by tests/test_recommender.py; delegates to the functions above."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for this profile via profile_to_prefs and recommend_songs."""
        raise NotImplementedError  # S3

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the reasons this song scores for this profile as one string."""
        raise NotImplementedError  # S3
