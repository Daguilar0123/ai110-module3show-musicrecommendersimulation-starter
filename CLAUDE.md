# CLAUDE.md: Music Recommender Simulation (CodePath AI110 Project 3)

A CLI-first, content-based recommender over `data/songs.csv` (20 songs). The design is decided and
recorded in `README.md` ("Algorithm recipe", "Dataset and profiles"); the contract is the skeleton in
`src/`. Plan, session table, merge commands and status: `MUSICREC_PLAN.md`.

## Working rules (this is for credit)
- Sessions propose, scaffold, explain and test. Danny reviews every diff and runs every git command.
- Danny writes: the `model_card.md` reflection and prose, the README "Reflection", and every
  `ai_interactions.md` write-up. A session may only tighten wording he wrote.
- Never commit, merge or push. Present exact `git add` / `git commit` commands with a memory-entry
  message (what changed, why, what was decided, dated). **No `Co-Authored-By` trailers.**
- STOP rule: show the diff at each named checkpoint and wait. "commit" is a literal word; commit
  commands are presented only after Danny types it.
- **No signature changes; STOP and report.** The coordinator decides and records it in `MUSICREC_PLAN.md`.
- Note side issues, don't fix them. One next step at a time for Danny.
- Every accepted or rejected AI suggestion gets a `#note` line in `notes/build_notes.md` (coordinator
  keeps the log at the bottom; format is described there).
- Read the real files first. If a plan number and the README disagree, the README wins; say so.

## Environment
- uv with Python 3.13 (`.python-version`): `uv venv`, `uv pip install -r requirements.txt`.
- Never plain `pip`, never `python3 -m venv`. `.venv/bin/python --version` prints 3.13.x.

## Run
- `.venv/bin/python -m src.main --all`
- `.venv/bin/python -m pytest -v` (run from the repo root; `-m` puts the root on `sys.path`)

## File map and owners
| File | Owner |
|---|---|
| `CLAUDE.md`, `MUSICREC_PLAN.md`, skeleton signatures, `#note` log | S0 coordinator |
| `data/songs.csv` | S0 (20 songs, done); S7 adds columns in wave 2 |
| `src/recommender.py`: `load_songs`, `tests/test_data.py` | S2 |
| `src/recommender.py`: `score_song`, `recommend_songs`, `profile_to_prefs`, `Recommender.*`, `tests/test_scoring.py` | S3 (S7 extends the `score_song` body only) |
| `src/main.py` bodies, `tests/test_cli.py`, README "Sample Recommendation Output" and "Experiments You Tried" | S4 |
| `src/ranking_modes.py`, `src/formatting.py`, `tests/test_modes.py`, `tests/test_table.py`, `tabulate` in `requirements.txt` | S5 |
| `src/diversity.py`, `tests/test_diversity.py` | S6 |
| new `songs.csv` columns, `tests/test_attributes.py` | S7 |
| README prose, `model_card.md`, `ai_interactions.md` write-ups | Danny |
| README "Getting Started", final sample-output refresh, submission checklist | S8 |
| `tests/test_recommender.py` (starter) | nobody edits |

Do not rename: `src/recommender.py`, `src/main.py`, `data/songs.csv`, `README.md`, `model_card.md`,
`ai_interactions.md`.

## Worktree workflow
- Each worker's first step: `git worktree add ../<name> -b <branch>` from the repo root, then all
  work stays inside that worktree. Branch and worktree names are in the session table in `MUSICREC_PLAN.md`.
- Workers never touch regions owned by another session. If two sessions seem to share a tree, stop and say so.

## Testing
- Every feature gets a targeted pytest that fails before and passes after.
- The two starter tests fail with `NotImplementedError` until S3 lands. That is expected.

## Style
- README describes in prose, never ticks boxes. A stretch item counts only with its write-up.
- Dates and attribution on decisions ("Danny confirms (Nov 2, 2026)...").
