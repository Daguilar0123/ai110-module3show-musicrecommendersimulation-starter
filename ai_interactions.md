# AI Interactions Log

> **Stretch features only.** 
## Stretch features attempted

All four optional Challenges were attempted. Two are written up in this file, as the starter asks; the other two are written up where the project page sends them. Links point to the exact sections.

### Challenge 1: Add Advanced Song Features (agentic workflow)

Five new song attributes, scored in `score_song`, built by an AI agent working on its own on branch `feat/attributes`. Written up below under **Agentic Workflow (SF8)**. Code: `feat/attributes` (commit `fd341e2`), not merged into `main` for this submission; see SF8 for why.

### Challenge 2: Create Multiple Scoring Modes (design pattern)

Four ranking modes (`weighted`, `genre_first`, `mood_first`, `energy_similarity`) switchable with `--mode`, built on a Strategy-style registry and factory. Written up below under **Design Pattern (SF10)**. Code: `src/ranking_modes.py`, `tests/test_modes.py`.

### Challenge 3: Diversity and Fairness Logic

An artist penalty (`--diversity`) that takes 0.5 off a song's score for every song by the same artist already in the list. Written up in the model card: [§6 Limitations and Bias](model_card.md#6-limitations-and-bias) (last paragraph) and [§8 Future Work](model_card.md#8-future-work). Code: `src/diversity.py`, `tests/test_diversity.py`.

### Challenge 4: Visual Summary Table

A `tabulate` table (`--table`) showing rank, title, artist, score and the reasons for each score. Written up in the README under [Visual Summary Table](README.md#visual-summary-table). Code: `src/formatting.py`, `tests/test_table.py`.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Challenge 1, "Add Advanced Song Features." I opened a separate Claude Code session in agent mode (accept edits), on its own branch `feat/attributes` in its own worktree, and gave it the whole job in one prompt: add five new columns to `data/songs.csv` for all 20 songs, make `load_songs` convert the numeric ones, add one clearly marked block to `score_song` that uses them, write a test for each new term, and keep a running record of every file it touched and every command it ran. I told it never to change a function signature or rename a column, and that I would review the full diff and run every git command myself.

**Prompts used:**

One opening prompt (about 100 lines), pasted Nov 3, 2026 at about 6:50 PM ET. The task part of it was:

> Add five columns to `data/songs.csv`, every row filled, plausible per song: `popularity` (int 0–100), `release_decade` (int, e.g. 1990, 2010, 2020), `mood_tags` (2–3 words separated by `|`), `explicit` (`yes`/`no`), `duration_sec` (int 120–420). Keep the existing ten columns and all 20 rows byte-identical otherwise.
> Add `popularity`, `release_decade` and `duration_sec` to `NUMERIC_FIELDS` so `load_songs` converts them. Do not touch `load_songs`.
> Extend `score_song`'s body with one clearly delimited block (`# --- extended attributes (S7) ---`) that only runs when the song has those keys: `+0.5 × popularity/100`; if the prefs contain `favorite_decade` and it matches, `+0.5`; if the prefs contain `mood_tags` and any tag overlaps the song's tags, `+0.5`; if prefs contain `avoid_explicit` True and the song is explicit, `-1.0`.

After that I sent no mid-task messages. The agent worked on its own (32 tool calls) and stopped at its checkpoint with the diff and the test output. My only other message was the word `commit`, Nov 4 at about 12:16 AM ET, after I had read the diff.

**What did the agent generate or change?**

Three files, 186 insertions and 22 deletions, committed as `fd341e2` on `feat/attributes`:

- `data/songs.csv`: five new columns (`popularity`, `release_decade`, `mood_tags`, `explicit`, `duration_sec`) on all 20 rows. The original ten columns are unchanged.
- `src/recommender.py`: three fields added to `NUMERIC_FIELDS`, and one delimited block in `score_song` with four terms: popularity up to +0.5, decade match +0.5, mood-tag overlap +0.5, and an explicit penalty of −1.0 when the profile sets `avoid_explicit`. Each term runs only when the key exists, so a song with the old ten columns scores exactly as before.
- `tests/test_attributes.py`: 7 tests, 138 lines.

Two decisions the agent made on its own, which I accepted: the new point values are fixed constants inside the block, not entries in `DEFAULT_WEIGHTS`, so no signature or contract changed; and a song with popularity 0 earns nothing and prints no reason, which matches the existing rule that no "+0.0" reason is ever printed.

**What did you verify or fix manually?**

- I ran the full suite in the worktree: 50 passed (the 43 from `main` plus the 7 new ones). The agent's own report said the same.
- I read the diff of all three files before typing `commit`. Nothing had to be fixed.
- The agent flagged two consequences I confirmed. Only the popularity term shows up in `--all`, because the profiles in `main.py` have no `favorite_decade`, `mood_tags` or `avoid_explicit` yet. And `load_songs` now raises `KeyError` on an old ten-column CSV.
- Running `--all` on the branch, the top five changes for `intense_rock`, `hiphop_fan` and `folk_acoustic`, and every score moves (for example `pop_happy`'s top score goes from 4.46 to 4.89 while its order holds). Because of that, every sample output in the README, the experiment blocks and model card §7 would go stale. So the branch is pushed but **not merged** for this submission. I will merge it, regenerate the outputs, and update this section in a resubmission.


---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy: interchangeable scoring functions behind one signature, chosen by name at run time.

**How did AI help you brainstorm or implement it?**

The ranking-modes session (prompt 05, Nov 3, 2026, about 1:35 AM) offered three ways to build `--mode`: a dict registry plus a small factory, a class hierarchy with one class per mode, or `functools.partial` over `score_song` with different weights. It recommended the registry for a 20-song command-line tool, and I picked it: the class hierarchy was noticeably more code for three modes that differ only in their weights, and `partial` was the shortest but hard to point at as a named pattern. The session then wrote the registry and seven tests red-first; I ran the suite and the live `--mode` runs myself before typing "commit". One correction worth recording: its closing report first credited me with the reasoning behind the choice, and the coordinator session corrected it, because I only picked the option.

**How does the pattern appear in your final code?**

`src/ranking_modes.py`: `MODE_WEIGHTS` is the registry (mode name to weight dict) and `get_scorer(mode)` is the factory. It returns a function with exactly `score_song`'s signature, so `recommend_songs(scorer=...)` and the `--mode` switch in `src/main.py` never know which strategy they were handed. The modes are weighted, genre_first, mood_first and energy_similarity.
