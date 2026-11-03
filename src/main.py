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
    "genre_half": {"genre": 0.5, "mood": 1.0, "energy": 1.0, "valence": 0.5, "acoustic": 0.5},
}


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """--profile NAME | --all · --k N (5) · --mode MODE (weighted) · --diversity [PENALTY] · --table · --experiment NAME"""
    parser = argparse.ArgumentParser(prog="python -m src.main", description="Music Recommender Simulation")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="pop_happy", help="which taste profile to run")
    parser.add_argument("--all", action="store_true", help="run every profile (overrides --profile)")
    parser.add_argument("--k", type=int, default=5, help="how many songs to recommend")
    parser.add_argument("--mode", default="weighted", help="ranking mode (weighted, genre_first, mood_first, energy_similarity)")
    parser.add_argument("--diversity", nargs="?", type=float, const=0.5, default=0.0, metavar="PENALTY",
                        help="artist-repeat penalty; bare --diversity means 0.5")
    parser.add_argument("--table", action="store_true", help="print a table instead of the reason lines")
    parser.add_argument("--experiment", choices=sorted(EXPERIMENTS), help="swap in an alternate weight set")
    args = parser.parse_args(argv)
    if args.experiment and args.mode != "weighted":
        parser.error("--experiment changes the weights, so it only works with --mode weighted")
    return args


def run_profile(name: str, prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "weighted",
                diversity: float = 0.0, table: bool = False, weights: Optional[Dict] = None) -> str:
    """Build the text block for one profile: header line, then rank/title/score/reasons per song (or the table when table=True)."""
    scorer = None
    if mode != "weighted":
        from src.ranking_modes import get_scorer   # lazy: the stub module is not needed for the default run
        scorer = get_scorer(mode)
    elif weights is not None:
        scorer = lambda p, s, w=None: score_song(p, s, weights)   # noqa: E731  (experiment: swap the weight dict)
    results = recommend_songs(prefs, songs, k, scorer=scorer, diversity_penalty=diversity)

    lines = [f"== {name}: genre={prefs['genre']}, mood={prefs['mood']}, energy={prefs['energy']} =="]
    if table:
        from src.formatting import format_table   # lazy, same reason
        lines.append(format_table(results))
    else:
        for rank, (song, score, explanation) in enumerate(results, start=1):
            lines.append(f"{rank}. {song['title']} — {song['artist']}  [{score:.2f}]")
            lines.append(f"   because: {explanation}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> None:
    """Load songs, print 'Loaded songs: N', run the chosen profile(s), print each block."""
    args = parse_args(argv)
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    names = list(PROFILES) if args.all else [args.profile]
    weights = EXPERIMENTS[args.experiment] if args.experiment else None
    for name in names:
        print()
        print(run_profile(name, PROFILES[name], songs, k=args.k, mode=args.mode,
                          diversity=args.diversity, table=args.table, weights=weights))


if __name__ == "__main__":
    main()
