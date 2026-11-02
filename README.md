# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version is a content-based music recommender that runs from the command line over a small CSV catalog. It scores each song against a listener's taste profile on genre, mood, energy, valence, and acousticness, then ranks the songs and explains each pick with a list of reasons.

---

## How The System Works

I believe Spotify does a combination of both. When you create a new account, Spotify and apps that serve content of some form, be it news, podcasts, Substack, Netflix, YouTube, etc., will ask a new user for their preferences. Usually you pick three or more artists you like. This is the beginning of building a user taste profile based on what I explicitly tell the app at the creation of my account. Then, based on that profile, it might first share what I like based on content-based filtering, but as I build a more organic profile, collaborative filtering gets used to introduce me to new songs or to fill out my taste profile if it is sparse.

If all we have is song data, then we have no choice but to do content-based filtering. The input data is the seven attribute columns of `data/songs.csv`: genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. The user preferences are a taste profile dictionary that stands in for the onboarding step, where a new listener picks artists they like. Collaborative filtering, which needs other users' behavior, is out of reach because we have no likes, skips, playlists, or listening history. The ranking has two parts. The Scoring Rule grades one song by itself: how well does it fit this listener? It's like a judge filling in a rubric for a single contestant. The Ranking Rule then looks at all the grades, lines the songs up from highest to lowest, and keeps the top few. A score alone can't tell you what to play, and a list can't be put in order without scores. So we need both.

### Features each Song uses

- genre
- mood
- energy
- valence
- acousticness

(`tempo_bpm` and `danceability` are loaded but not scored in v1.)

### What a UserProfile stores

- favorite genre
- favorite mood
- target energy
- target valence
- likes_acoustic

### Algorithm recipe (decided Nov 2, 2026)

- Genre match: +2.0. A partial match, where one genre string contains the other (case-insensitive, e.g. "indie pop" vs "pop"), earns +1.0.
- Mood match: +1.0.
- Energy closeness: 1.0 × (1 − |song energy − target energy|).
- Valence closeness: 0.5 × (1 − |song valence − target valence|), applied only when the profile has a valence target.
- Acoustic bonus: +0.5 when the profile's `likes_acoustic` agrees with the song's acousticness > 0.5.
- `tempo_bpm` and `danceability` are not scored in v1.
- Every score comes with a list of reasons.

Closeness is `1 − |song − target|`, so the closer a song is to the target, the higher it scores, whether the song is above or below. Worked example with a target energy of 0.8: a song at 0.82 scores 0.98, a song at 0.42 scores 0.62, and a song at 0.28 scores 0.48.

### Why genre weighs the most, and the bias I expect

Most people describe the kind of music they like first and foremost by genre. People don't say "I like high-energy or low-valence music"; they say "I like hip hop, pop, country or classical." So genre is the label a listener gives, and the numeric features are how the system tells songs apart inside that label. Because genre is worth +2.0, this system might over-prioritize genre and ignore great songs that match the user's mood and energy. That is a bias I chose on purpose, and the weight-shift experiment later is where I test it.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



