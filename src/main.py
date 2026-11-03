"""Command line runner for the Music Recommender Simulation (python -m src.main)."""
import argparse
from typing import Dict, List, Optional
try:
    from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs, score_song
except ImportError:  # running as `python src/main.py`
    from recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs, score_song

PROFILES: Dict[str, Dict] = {
    "pop_happy": {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8},
    "chill_lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.6, "likes_acoustic": True},
    "intense_rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.45},
    "hiphop_fan": {"genre": "hip-hop", "mood": "confident", "energy": 0.75, "valence": 0.65},
    "conflicted": {"genre": "pop", "mood": "sad", "energy": 0.9, "valence": 0.3},
    "folk_acoustic": {"genre": "folk", "mood": "hopeful", "energy": 0.45, "valence": 0.7, "likes_acoustic": True},
}
EXPERIMENTS: Dict[str, Dict[str, float]] = {   # weight variants for Phase 4 Step 3
    "weight_shift": {"genre": 1.0, "mood": 1.0, "energy": 2.0, "valence": 0.5, "acoustic": 0.5},
    "no_mood": {"genre": 2.0, "mood": 0.0, "energy": 1.0, "valence": 0.5, "acoustic": 0.5},
}


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """--profile NAME | --all · --k N (5) · --mode MODE (weighted) · --diversity [PENALTY] · --table · --experiment NAME"""
    raise NotImplementedError  # S4


def run_profile(name: str, prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "weighted",
                diversity: float = 0.0, table: bool = False, weights: Optional[Dict] = None) -> str:
    """Build the text block for one profile: header line, then rank/title/score/reasons per song (or the table when table=True)."""
    raise NotImplementedError  # S4


def main(argv: Optional[List[str]] = None) -> None:
    """Load songs, print 'Loaded songs: N', run the chosen profile(s), print each block."""
    raise NotImplementedError  # S4


if __name__ == "__main__":
    main()
