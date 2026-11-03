"""Strategy pattern: interchangeable scoring functions behind one signature.

Every mode is a scorer with score_song's signature (user_prefs, song, weights=None). MODE_WEIGHTS is the
registry (mode name -> weight dict) and get_scorer is the one small factory, so main.py's --mode switch
and recommend_songs(scorer=...) never need to know which strategy they were handed.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict

try:
    from src.recommender import score_song
except ImportError:  # running as `python src/main.py`
    from recommender import score_song

if TYPE_CHECKING:
    from src.recommender import Scorer

MODES = ("weighted", "genre_first", "mood_first", "energy_similarity")

# Registry: every dict names all five weight keys. "weighted" is absent on purpose; it is score_song itself.
MODE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "genre_first": {"genre": 5.0, "mood": 1.0, "energy": 0.5, "valence": 0.25, "acoustic": 0.25},
    "mood_first": {"genre": 0.5, "mood": 5.0, "energy": 0.5, "valence": 0.25, "acoustic": 0.25},
    "energy_similarity": {"genre": 0.0, "mood": 0.0, "energy": 5.0, "valence": 0.0, "acoustic": 0.0},
}


def get_scorer(mode: str) -> Scorer:
    """Return the scorer for mode; 'weighted' is score_song itself; unknown mode raises ValueError."""
    if mode == "weighted":
        return score_song
    if mode not in MODE_WEIGHTS:
        raise ValueError(f"Unknown ranking mode '{mode}'. Choose one of: {', '.join(MODES)}")
    mode_weights = MODE_WEIGHTS[mode]

    def scorer(user_prefs, song, weights=None):
        """score_song with this mode's weights; an explicit weights argument wins when it is not None."""
        return score_song(user_prefs, song, mode_weights if weights is None else weights)

    scorer.__name__ = f"{mode}_scorer"
    return scorer
