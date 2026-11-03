"""CLI tests (S4). Everything the CLI calls is monkeypatched, so these run before merge 1."""
import src.main as cli

FAKE_SONGS = [
    {"id": 1, "title": "Sunrise City", "artist": "Neon Echo", "genre": "pop", "mood": "happy",
     "energy": 0.82, "tempo_bpm": 118.0, "valence": 0.84, "danceability": 0.79, "acousticness": 0.18},
    {"id": 2, "title": "Midnight Coding", "artist": "LoRoom", "genre": "lofi", "mood": "chill",
     "energy": 0.42, "tempo_bpm": 78.0, "valence": 0.56, "danceability": 0.62, "acousticness": 0.71},
    {"id": 3, "title": "Storm Runner", "artist": "Voltline", "genre": "rock", "mood": "intense",
     "energy": 0.91, "tempo_bpm": 152.0, "valence": 0.48, "danceability": 0.66, "acousticness": 0.10},
]
FAKE_SCORES = (3.0, 2.0, 1.0)
FAKE_REASONS = ("genre match (+2.0)", "mood match (+1.0)", "energy closeness (+0.5)")


def fake_recommend(prefs, songs, k=5, scorer=None, diversity_penalty=0.0):
    """Stand-in for recommend_songs: calls the scorer once per song (so tests can spy on it), returns fixed results."""
    if scorer is not None:
        for song in songs:
            scorer(prefs, song)
    return [(song, score, reason) for song, score, reason in zip(songs, FAKE_SCORES, FAKE_REASONS)][:k]


def patch_cli(monkeypatch):
    monkeypatch.setattr(cli, "load_songs", lambda path: list(FAKE_SONGS))
    monkeypatch.setattr(cli, "recommend_songs", fake_recommend)


def test_profiles_has_at_least_three_distinct():
    assert len(cli.PROFILES) >= 3
    pairs = {(p["genre"], p["mood"]) for p in cli.PROFILES.values()}
    assert len(pairs) == len(cli.PROFILES)


def test_all_profiles_run(monkeypatch, capsys):
    patch_cli(monkeypatch)
    cli.main(["--all"])
    out = capsys.readouterr().out
    assert "Loaded songs: 3" in out
    headers = [line for line in out.splitlines() if line.startswith("== ")]
    assert len(headers) == len(cli.PROFILES)
    for name in cli.PROFILES:
        assert f"== {name}:" in out


def test_output_shows_title_score_and_reasons(monkeypatch, capsys):
    patch_cli(monkeypatch)
    cli.main(["--profile", "pop_happy"])
    out = capsys.readouterr().out
    assert "Sunrise City" in out
    assert "[3.00]" in out
    assert "because:" in out


def test_parse_args_defaults():
    args = cli.parse_args([])
    assert args.profile == "pop_happy"
    assert args.k == 5
    assert args.mode == "weighted"
    assert args.diversity == 0.0
    assert args.table is False
    assert args.all is False
    assert args.experiment is None


def test_experiment_passes_weights(monkeypatch, capsys):
    patch_cli(monkeypatch)
    seen = []

    def spy_score_song(prefs, song, weights=None):
        seen.append(weights)
        return 1.0, ["spy"]

    monkeypatch.setattr(cli, "score_song", spy_score_song)
    cli.main(["--profile", "pop_happy", "--experiment", "weight_shift"])
    assert seen, "the scorer was never called"
    assert all(w == cli.EXPERIMENTS["weight_shift"] for w in seen)


def test_genre_half_experiment_is_selectable():
    assert cli.EXPERIMENTS["genre_half"] == {"genre": 0.5, "mood": 1.0, "energy": 1.0, "valence": 0.5, "acoustic": 0.5}
    assert cli.parse_args(["--experiment", "genre_half"]).experiment == "genre_half"
