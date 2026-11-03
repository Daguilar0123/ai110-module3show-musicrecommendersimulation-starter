# MUSICREC_PLAN.md: sessions, merges and status

Owner: S0 coordinator (`musicrec-coordinator`). Copied from the study-repo build plan on Nov 2, 2026.
The contract is the skeleton in `src/`; the decided values are in `README.md`. Where they disagree, the README wins.

## Data flow
- Input: the profile's prefs dict (genre, mood, energy, optional valence and likes_acoustic).
- Process: `score_song` for every CSV row, then sort by score.
- Output: the top k as (song, score, reasons). See `diagrams/data_flow.mmd`.

## Sessions and waves

| Wave | # | Course phase | Branch → worktree | Owns (nobody else touches) | Prompt |
|---|---|---|---|---|---|
| 0 | S0 | Coordinator; Phase 1 and 2; skeleton commit; all merges and gates | `main`, repo root | `CLAUDE.md`, `MUSICREC_PLAN.md`, `.python-version`, skeleton edits to `src/recommender.py`, `src/main.py`, stub files `src/ranking_modes.py`, `src/diversity.py`, `src/formatting.py`; `#note` log in `ai_interactions.md` | `00_Coordinator.md` |
| 1 | S2 | Phase 3 Step 1: `load_songs` | `feat/data` → `../musicrec-data` | `load_songs` body, `tests/test_data.py` | `02_Data.md` |
| 1 | S3 | Phase 3 Steps 2, 3, 5: scoring, ranking, explanations, docstrings | `feat/scoring` → `../musicrec-scoring` | `score_song`, `recommend_songs`, `profile_to_prefs`, `Recommender.recommend`, `Recommender.explain_recommendation` bodies, `tests/test_scoring.py` | `03_Scoring.md` |
| 1 | S4 | Phase 3 Step 4 + Phase 4 Steps 1–3: CLI, profiles, output format, weight-shift experiment | `feat/cli` → `../musicrec-cli` | `src/main.py` bodies (`PROFILES`, `parse_args`, `run_profile`, `main`), `tests/test_cli.py`, README "Sample Recommendation Output" and "Experiments You Tried", output blocks in `model_card.md` §7 | `04_CLI_Profiles.md` |
| merge 1 | Danny | `feat/data` → `feat/scoring` → (S4 merges `main`, live check) → `feat/cli`; then `python -m src.main --all` and `pytest -v` on `main`; push | | | S0 gives the commands |
| 2 | S5 | Challenge 2 + 4: Strategy ranking modes and the tabulate table | `experiment/mood-first` → `../musicrec-modes` | `src/ranking_modes.py`, `src/formatting.py`, `tests/test_modes.py`, `tests/test_table.py`, `tabulate` in `requirements.txt` | `05_Stretch_Modes_Table.md` |
| 2 | S6 | Challenge 3: diversity penalty | `feat/diversity` → `../musicrec-diversity` | `src/diversity.py`, `tests/test_diversity.py` | `06_Stretch_Diversity.md` |
| 2 | S7 | Challenge 1, agent mode: five new attributes | `feat/attributes` → `../musicrec-attributes` | new columns in `data/songs.csv`, new-attribute block inside `score_song` (body only), `tests/test_attributes.py` | `07_Stretch_Attributes_AgentMode.md` |
| 2 | Danny | README "How The System Works" polish, `model_card.md` §1–§9, reflection answers, SF8/SF10 write-ups | repo root, on `main` | `README.md` prose sections, `model_card.md`, `ai_interactions.md` stretch sections | `09_Danny_Explanations_and_Model_Card.md` |
| merge 2 | Danny | `feat/diversity` → `experiment/mood-first` → `feat/attributes`; full pytest; table run; push | | | S0 gives the commands |
| 3 | S8 | Phase 5 polish and submit | `main`, no worktree | README "Getting Started" (uv), "Testing" block, final sample-output refresh, placeholder grep, worktree removal, submission checklist | `08_Polish_and_Submit.md` |

## Merge commands (Danny runs them from the repo root, after the coordinator's go-ahead)

Merge 1, in this order:
```
git checkout main
git merge --no-ff feat/data -m "Merge feat/data: 20-song catalog and load_songs with numeric conversion (S2)"
git merge --no-ff feat/scoring -m "Merge feat/scoring: score_song with reasons, recommend_songs top-k, OOP bridge (S3)"
```
Then tell S4 **"main has data and scoring"**; S4 runs `git merge main` inside `../musicrec-cli`, does its
live check, and Danny commits there. Then:
```
git merge --no-ff feat/cli -m "Merge feat/cli: working CLI-first simulation; six profiles, flags, formatted output, weight-shift experiment (S4)"
.venv/bin/python -m src.main --all
.venv/bin/python -m pytest -v
git push origin main
```
Merge 2, in this order (each branch was started from merge-1 `main`):
```
git checkout main
git merge --no-ff feat/diversity -m "Merge feat/diversity: artist penalty re-ranking behind --diversity (S6)"
git merge --no-ff experiment/mood-first -m "Merge experiment/mood-first: Strategy ranking modes and tabulate table (S5)"
git merge --no-ff feat/attributes -m "Merge feat/attributes: five new song attributes scored, agent-mode session (S7)"
.venv/bin/python -m pytest -v
.venv/bin/python -m src.main --all --table --mode genre_first --diversity
git push origin main
```
Predicted conflict zones: none by design in `src/*.py`. If a conflict appears, the coordinator shows both sides.

## Deviations from the study-repo plan (decided Nov 2, 2026; README wins)
- `EXPERIMENTS` weight sets include `"valence": 0.5`. The plan's block omitted it.
- `PROFILES` holds six profiles (the README table), not one. The folk_acoustic profile is new.
- `main.py` imports `score_song` as well as `DEFAULT_WEIGHTS`, `load_songs`, `recommend_songs`.

Worker prompts 02-06 were corrected at the source in the study repo (commit 4618577, Nov 2, 2026, ~8:30 PM) after the cross-check logged in ai_interactions.md.

## Status

### S0
started 19:54

### S2
started 20:05; committed 7189eac on feat/data (22:29, verified); ready for merge 1

### S3
started 20:05; STOP 1 reviewed 21:51 (diff correct, 14 passed); waiting on Step 3

### S4
started 20:05; STOP 1 reviewed 21:51 (diff correct, 5 passed); parked until 'main has data and scoring'

### S5
not started

### S6
not started

### S7
not started

### S8
not started

### Danny-09
not started
