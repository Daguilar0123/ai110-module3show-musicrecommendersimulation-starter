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
    raise NotImplementedError  # S2 load_songs


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Score one song against user_prefs; returns (score, reasons) using weights or DEFAULT_WEIGHTS."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}   # a partial weights dict fills its gaps from the defaults
    score = 0.0                                  # float on purpose: round(0, 4) would hand back an int
    reasons: List[str] = []

    want_genre = str(user_prefs.get("genre") or "").strip().lower()
    have_genre = str(song.get("genre") or "").strip().lower()
    if want_genre and have_genre and w["genre"] != 0:   # a zero weight leaves the term, and its reason, out
        if want_genre == have_genre:
            score += w["genre"]
            reasons.append(f"genre match (+{w['genre']:.1f})")
        elif want_genre in have_genre or have_genre in want_genre:   # "pop" vs "indie pop"
            half = w["genre"] / 2
            score += half
            reasons.append(f"genre partial match (+{half:.1f})")

    want_mood = str(user_prefs.get("mood") or "").strip().lower()
    if want_mood and w["mood"] != 0 and want_mood == str(song.get("mood") or "").strip().lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None and w["energy"] != 0:
        closeness = 1 - abs(song["energy"] - target_energy)   # unweighted, so the word does not depend on the weight
        points = w["energy"] * closeness
        score += points
        label = "close to" if closeness >= 0.5 else "far from"
        reasons.append(f"energy {label} target (+{points:.2f})")

    target_valence = user_prefs.get("valence")   # no target in the profile: the term is skipped
    if target_valence is not None and w["valence"] != 0:
        closeness = 1 - abs(song["valence"] - target_valence)
        points = w["valence"] * closeness
        score += points
        label = "close to" if closeness >= 0.5 else "far from"
        reasons.append(f"valence {label} target (+{points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")   # absent: no bonus either way
    if likes_acoustic is not None and w["acoustic"] != 0 and bool(likes_acoustic) == (song["acousticness"] > 0.5):
        score += w["acoustic"]
        reasons.append(f"acoustic fit (+{w['acoustic']:.1f})")

    if not reasons:
        reasons.append("no feature matched (+0.0)")
    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    scorer: Optional[Scorer] = None, diversity_penalty: float = 0.0) -> List[Tuple[Dict, float, str]]:
    """Score every song with scorer (default score_song), apply the artist penalty if > 0, return the top k as (song, score, explanation).
    sorted() returns a new list and leaves the original alone, while list.sort() reorders in place and returns None; both are stable, so ties keep CSV order."""
    scorer = scorer or score_song
    scored = []
    for song in songs:
        score, reasons = scorer(user_prefs, song)
        scored.append((song, score, reasons))
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    if diversity_penalty > 0:   # the default path never touches S6's stub
        try:
            from src.diversity import apply_artist_penalty
        except ImportError:  # running as `python src/main.py`
            from diversity import apply_artist_penalty
        ranked = apply_artist_penalty(ranked, diversity_penalty)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]


def profile_to_prefs(user: UserProfile) -> Dict:
    """Bridge the OOP profile to the functional dict: genre, mood, energy, likes_acoustic."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """OOP wrapper required by tests/test_recommender.py; delegates to the functions above."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for this profile via profile_to_prefs and recommend_songs."""
        results = recommend_songs(profile_to_prefs(user), [asdict(s) for s in self.songs], k)
        by_id = {s.id: s for s in self.songs}
        return [by_id[d["id"]] for d, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the reasons this song scores for this profile as one string."""
        score, reasons = score_song(profile_to_prefs(user), asdict(song))
        return f"{song.title}: {score:.2f} — " + "; ".join(reasons)
