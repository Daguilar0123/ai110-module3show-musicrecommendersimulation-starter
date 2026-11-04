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
started 19:54; wave 1 merged and pushed 00:28; wave 2 (S5, S6) started about 01:30

### S2
started 20:05; committed 7189eac; merged e85b047; merge 1 complete and pushed (00:28): main b40ba07, 28 passed

### S3
started 20:05; committed 91a1c2e; merged a3fb91d; merge 1 complete and pushed (00:28)

### S4
started 20:05; committed 14cae76; merged b40ba07; merge 1 complete and pushed (00:28); closing report requested

### S5
started about 01:32; committed d1d8ff1; merged into main in merge 2 (16:02); main 42 passed; write-ups (table paragraphs, design-pattern note) are Danny's

### S6
started about 01:28; committed 24c4f50; merged into main in merge 2 (16:02); main 42 passed; fairness paragraph is Danny's

### S7
started about 18:48 in agent mode; committed fd341e2 on feat/attributes (50 passed); NOT merged into main for the first submit (it changes every profile's scores and would stale the README, experiment and model card outputs); SF8 written by Danny; merge or leave for the resubmit

### S8
no separate session; the coordinator did the polish on main (README Getting Started and Running Tests, placeholder sweep, committed 174fba5); first portal submit reported by Danny Nov 4, 2026 (about 1:40-1:50 AM ET), grade not yet seen

### Danny-09
README limitations, reflection and Visual Summary Table, model card 1-9, SF8 and SF10 written by Danny (Nov 4, 2026); the polish work (S8) is done by the coordinator on main, docs only
