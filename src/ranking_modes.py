"""Strategy-pattern ranking modes: a registry of scorers that all share score_song's signature."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.recommender import Scorer

MODES = ("weighted", "genre_first", "mood_first", "energy_similarity")


def get_scorer(mode: str) -> Scorer:
    """Return the scorer for mode; 'weighted' is score_song itself; unknown mode raises ValueError."""
    raise NotImplementedError  # S5
