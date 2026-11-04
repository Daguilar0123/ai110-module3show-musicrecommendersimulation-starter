# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**Sad But Loud 1.0** (named after the profile that taught me the most). A content-based music recommender that scores 20 invented songs against one listener's taste profile and explains every pick.

---

## 2. Intended Use

This recommender takes one taste profile (a favorite genre, a favorite mood, a target energy, optionally a target valence and whether the listener likes acoustic sound) and returns the five songs from a 20-song catalog that fit it best, each with the reasons for its score. It assumes a listener can describe their taste as a single profile, that genre is the first word they would use for it, and that a song's fit can be summed from a handful of attributes. It is built for classroom exploration of how a recommender turns data into predictions. It is not for real listeners: the songs are invented, the catalog is too small to filter by genre, and it never actually learns from what anyone plays.

---

## 3. How the Model Works

Each song carries a few facts: its genre, its mood, and numbers between 0 and 1 for how energetic, how happy-sounding, and how acoustic it is. The listener's profile carries the same kinds of facts as targets. The scoring rule grades one song at a time, like a judge filling in a rubric for a single contestant. A matching genre is worth the most, two points, or one point if the names overlap the way "pop" and "indie pop" do. A matching mood is worth one point. Energy and happiness are scored by closeness: one minus the gap between the song and the target, so a song slightly above and a song slightly below the target earn the same, and an exact match earns full credit; energy counts in full and happiness counts at half, and only when the profile names a target. If the listener said they like acoustic sound and the song is acoustic, half a point more. The points add up to one score, and every term that earned points writes one reason line. The ranking rule then lines up all twenty scores, highest first, and keeps the top five. The starter had no logic at all, only empty functions; I decided the recipe, added the reasons, the six profiles, the command-line flags, and three experiments that swap the weights. This is content-based filtering in the cold-start state: the profile stands in for the artists a new user picks at sign-up, and nothing is learned afterward, because the catalog has no listening data.

---

## 4. Data

The catalog is 20 invented songs with ten columns each: id, title, artist, genre, mood, energy, tempo, valence, danceability and acousticness. The starter shipped 10; I approved 10 more (ids 11 to 20) on Nov 2 to cover genres the starter lacked and to fill an empty band of energy between 0.43 and 0.74. There are 16 genres (pop and lofi have three songs each, every other genre has one) and 14 moods, and two artists, Neon Echo and LoRoom, appear three times each on purpose so the diversity penalty has something to act on. Energy runs from 0.18 to 0.97. I score five of the columns; tempo and danceability are loaded but unused, because on this catalog they mostly repeat energy. Nothing in the data is behavior: no plays, skips, likes, playlists or listening history, which is why collaborative filtering is impossible here. Nothing is measured from audio either; every number is what the row's author imagined, and the genre and mood words are that author's opinion.

---

## 5. Strengths

For every one of the six profiles, the song that matches both labels comes first, and the because line says why in a way I can check by hand: Sunrise City for pop_happy, Library Rain for chill_lofi, Storm Runner for intense_rock, Crown Math for hiphop_fan, Porch Light Hymn for folk_acoustic. The two profiles I built as opposites, intense_rock and chill_lofi, share no songs at all, which matched my intuition exactly. chill_lofi's whole top five is low-energy and acoustic, so the acoustic bonus does what I meant it to do. The closeness rule captures something real: a song at energy 0.82 against a target of 0.8 scores almost perfectly, while a song at 0.28 scores about half, and neither direction is punished more than the other. And the experiments are cheap to run, which made the system easy to question.

---

## 6. Limitations and Bias

The biggest limitation is that genre is worth 2 of the 5 possible points, and this catalog is too small for that to work the way I meant it. In my opinion a genre-first bias is what I want as a listener: when I am in a hip-hop profile I want to be exposed to new songs, but I do not want classical to play. With millions of songs, genre can act as a gate and the numbers can rank what is inside it. With only 20 songs across 16 genres, three of my six profiles (rock, hip-hop, folk) have exactly one song of their genre, so the weight hands that song a 2.0-point head start and then has nothing left to reward; the other four slots are filled by off-genre songs on numbers alone. The research I had done on Spotify found that it does not score by genre at all: genre emerges from the audio and from which songs people play and playlist together, which I found interesting, because it means my genre weight is a shortcut for signals a real system learns. Where a genre has three songs, the weight does dominate: for pop_happy, Rain on the Radio, a slow sad pop song, sat 1.51 points above Fuego en la Calle, a loud happy latin song that fits the numbers better. It should not have: pop_happy asks for energy 0.8 and valence 0.8, Fuego sits at 0.80 and 0.86, almost a perfect fit, while Rain sits at 0.55 and 0.25, and the only thing Rain had going for it was the word "pop". Cutting the genre weight in half collapsed that lead to 0.01. In a quick extra run with the genre weight set to zero, Rain on the Radio still won the conflicted profile on its mood match, but Gym Hero and Sunrise City dropped out of the top five and Iron Verdict, Storm Runner and Night Drive Loop, the loud songs it was asking for, came in.

This is the small version of a filter bubble: the system keeps showing more of the same label, and Spotify's own 2020 study found algorithm-driven listening is less diverse than organic listening. A second limitation is the labels themselves: genre and mood are opinions typed by whoever wrote the row, the songs are invented, and numbers like valence are what the author imagined rather than measurements of audio; with only five scored features, genre is also standing in for the hundreds of audio and behavior signals a real system has.

The diversity penalty (Challenge 3) is my one counter-measure. When --diversity is on, a song whose artist already appears higher in the list loses 0.5 points per repeat and the list is re-sorted, so one artist cannot fill the top five. For the hiphop_fan profile this turned four artists into five: Sunrise City, the second Neon Echo song, dropped out and Velvet Hours by Marlo Reyes came in. The cost is fairness bought with a little accuracy: Velvet Hours at 1.29 is shown above Sunrise City at 1.33, a slightly weaker match ahead of a better one. The penalty knows nothing about what anyone played; it only looks at the list it is building.

---

## 7. Evaluation

I tested six taste profiles: pop_happy, chill_lofi, intense_rock, hiphop_fan, folk_acoustic, and one deliberately conflicting profile, conflicted (pop, sad, energy 0.9), that I describe as "sad but loud" because its labels and its numbers pull in opposite directions. For each one I ran `python -m src.main --all` and asked three things of the top five: does the first song match both labels, do the next four make sense for that listener, and does the because line explain the score in a way I can check by hand. I also ran three weight experiments (weight_shift, no_mood, genre_half), the diversity penalty on every profile, and the 43 automated tests after every merge; the coordinator session separately re-computed all 360 scores (6 profiles times 20 songs times 3 weight sets) with its own formula and got 0 mismatches.

What surprised me most was conflicted. I expected the loud songs to win because energy 0.9 is an extreme ask, but Rain on the Radio, a 0.55-energy song, came first, because it is the only pop and sad song in the catalog and the two labels are worth 3.0 points together. Empty Hall Etude, a classical piece at energy 0.18, even made the top five on the mood match alone. The second surprise was how little moved under weight_shift: pop_happy kept the same five songs in the same order and only the scores changed. The third was hiphop_fan: after Crown Math, the only hip-hop song, slots two through five are within 0.13 points of each other, decided by energy and valence alone, which is why a 0.5 diversity penalty was enough to reshuffle them.

Profile `pop_happy`, top 5 (`python -m src.main --all`, Nov 2, 2026):

```
== pop_happy: genre=pop, mood=happy, energy=0.8 ==
1. Sunrise City — Neon Echo  [4.46]
   because: genre match (+2.0); mood match (+1.0); energy close to target (+0.98); valence close to target (+0.48)
2. Rooftop Lights — Indigo Parade  [3.46]
   because: genre partial match (+1.0); mood match (+1.0); energy close to target (+0.96); valence close to target (+0.49)
3. Gym Hero — Max Pulse  [3.35]
   because: genre match (+2.0); energy close to target (+0.87); valence close to target (+0.48)
4. Rain on the Radio — June Alder  [2.98]
   because: genre match (+2.0); energy close to target (+0.75); valence far from target (+0.22)
5. Fuego en la Calle — Luna Caliente  [1.47]
   because: energy close to target (+1.00); valence close to target (+0.47)
```

Profile `chill_lofi`, top 5 (`python -m src.main --all`, Nov 2, 2026):

```
== chill_lofi: genre=lofi, mood=chill, energy=0.35 ==
1. Library Rain — Paper Lanterns  [5.00]
   because: genre match (+2.0); mood match (+1.0); energy close to target (+1.00); valence close to target (+0.50); acoustic fit (+0.5)
2. Midnight Coding — LoRoom  [4.91]
   because: genre match (+2.0); mood match (+1.0); energy close to target (+0.93); valence close to target (+0.48); acoustic fit (+0.5)
3. Focus Flow — LoRoom  [3.94]
   because: genre match (+2.0); energy close to target (+0.95); valence close to target (+0.49); acoustic fit (+0.5)
4. Spacewalk Thoughts — Orbit Bloom  [2.90]
   because: mood match (+1.0); energy close to target (+0.93); valence close to target (+0.47); acoustic fit (+0.5)
5. Coffee Shop Stories — Slow Stereo  [1.93]
   because: energy close to target (+0.98); valence close to target (+0.45); acoustic fit (+0.5)
```

Profile `intense_rock`, top 5 (`python -m src.main --all`, Nov 2, 2026):

```
== intense_rock: genre=rock, mood=intense, energy=0.9 ==
1. Storm Runner — Voltline  [4.47]
   because: genre match (+2.0); mood match (+1.0); energy close to target (+0.99); valence close to target (+0.48)
2. Gym Hero — Max Pulse  [2.31]
   because: mood match (+1.0); energy close to target (+0.97); valence close to target (+0.34)
3. Night Drive Loop — Neon Echo  [1.33]
   because: energy close to target (+0.85); valence close to target (+0.48)
4. Iron Verdict — Iron Hollow  [1.33]
   because: energy close to target (+0.93); valence close to target (+0.40)
5. Crown Math — Kid Cadence  [1.25]
   because: energy close to target (+0.86); valence close to target (+0.39)
```

Profile `hiphop_fan`, top 5 (`python -m src.main --all`, Nov 2, 2026):

```
== hiphop_fan: genre=hip-hop, mood=confident, energy=0.75 ==
1. Crown Math — Kid Cadence  [4.47]
   because: genre match (+2.0); mood match (+1.0); energy close to target (+0.99); valence close to target (+0.48)
2. Night Drive Loop — Neon Echo  [1.42]
   because: energy close to target (+1.00); valence close to target (+0.42)
3. Rooftop Lights — Indigo Parade  [1.41]
   because: energy close to target (+0.99); valence close to target (+0.42)
4. Fuego en la Calle — Luna Caliente  [1.34]
   because: energy close to target (+0.95); valence close to target (+0.40)
5. Sunrise City — Neon Echo  [1.33]
   because: energy close to target (+0.93); valence close to target (+0.41)
```

Profile `conflicted`, top 5 (`python -m src.main --all`, Nov 2, 2026):

```
== conflicted: genre=pop, mood=sad, energy=0.9 ==
1. Rain on the Radio — June Alder  [4.12]
   because: genre match (+2.0); mood match (+1.0); energy close to target (+0.65); valence close to target (+0.47)
2. Gym Hero — Max Pulse  [3.23]
   because: genre match (+2.0); energy close to target (+0.97); valence close to target (+0.27)
3. Sunrise City — Neon Echo  [3.15]
   because: genre match (+2.0); energy close to target (+0.92); valence far from target (+0.23)
4. Rooftop Lights — Indigo Parade  [2.10]
   because: genre partial match (+1.0); energy close to target (+0.86); valence far from target (+0.24)
5. Empty Hall Etude — LoRoom  [1.74]
   because: mood match (+1.0); energy far from target (+0.28); valence close to target (+0.46)
```

Profile `folk_acoustic`, top 5 (`python -m src.main --all`, Nov 2, 2026):

```
== folk_acoustic: genre=folk, mood=hopeful, energy=0.45 ==
1. Porch Light Hymn — Willow Mere  [5.00]
   because: genre match (+2.0); mood match (+1.0); energy close to target (+1.00); valence close to target (+0.50); acoustic fit (+0.5)
2. Salt Tide — Salt Tide Collective  [1.93]
   because: energy close to target (+0.97); valence close to target (+0.46); acoustic fit (+0.5)
3. Coffee Shop Stories — Slow Stereo  [1.92]
   because: energy close to target (+0.92); valence close to target (+0.49); acoustic fit (+0.5)
4. Midnight Coding — LoRoom  [1.90]
   because: energy close to target (+0.97); valence close to target (+0.43); acoustic fit (+0.5)
5. Focus Flow — LoRoom  [1.90]
   because: energy close to target (+0.95); valence close to target (+0.45); acoustic fit (+0.5)
```

Comparing the profiles in pairs shows what the preferences are actually testing for. intense_rock and chill_lofi share no songs at all: their energy targets are 0.9 and 0.35, so every song that is close for one is far for the other, and the acoustic bonus only chill_lofi can earn pushes Library Rain to a perfect 5.00 while Storm Runner leads the rock list at 4.47. pop_happy and conflicted share four of five songs because they share the genre pop, but the order flips on mood: Rain on the Radio is fourth for pop_happy and first for conflicted because "sad" matches it, while Sunrise City drops from first to third once "happy" no longer counts. chill_lofi and folk_acoustic share three songs (Midnight Coding, Focus Flow, Coffee Shop Stories) because both are low-energy acoustic listeners; the lofi songs lose their genre and mood points for folk_acoustic and fall from 4.91 and 3.94 to 1.90 each, held up only by closeness and the acoustic bonus. pop_happy and hiphop_fan look alike on the numbers (energy 0.8 versus 0.75, valence 0.8 versus 0.65) and share three songs, but the labels separate them completely at the top: Sunrise City is first for one and fifth for the other. The pattern I see across all six is that the first slot is decided by the labels and the rest of the list is decided by the numbers, and the numbers only get a real say when the catalog has more than one song of the profile's genre.

The experiments confirmed that. weight_shift (energy 2.0, genre 1.0) left pop_happy's list unchanged and only moved the gaps, but for conflicted it brought Storm Runner into the top five and pushed Empty Hall Etude from fifth to tenth, which is the list I originally expected for a loud profile. no_mood took Rain on the Radio's win away from conflicted and gave it to Gym Hero. genre_half kept pop_happy's order but shrank Rain's lead over Fuego en la Calle from 1.51 to 0.01, the number I use in the Limitations section. None of the experiments made the recommendations more accurate for every profile at once; they made them different, and each one exposed which single term had been deciding a slot.

---

## 8. Future Work

First, more songs per genre, so that genre can work as a gate the way I intended instead of deciding one slot and going quiet; that is the direct fix for the limitation above. Second, a two-cluster taste profile: a primary and a secondary preference dict with weights like 0.7 and 0.3, scoring each song against both and keeping the higher weighted result, so a listener who likes hip-hop and also likes folk is not forced into one profile. Third, richer song features, which the attributes extension starts tonight with popularity, release decade, mood tags, an explicit flag and duration; Pandora labels about 400 traits per song, and I score 5. If I kept going I would also tune the diversity penalty so it can penalize a repeated genre as well as a repeated artist, and print the margin between first and second place so a reader can see when a pick was decided by a single label.

---

## 9. Personal Reflection

My biggest learning moment was understanding that a recommender needs two separate rules and why. The scoring rule gives one song a single number from several features, and the ranking rule puts twenty of those numbers in order and cuts the list; a score alone cannot tell you what to play, and a list cannot be ordered without scores. Once that clicked, the whole program read as load, pick, loop, score, sort, cut, join, print.

AI did most of the typing and I did the deciding. The sessions proposed the recipe, wrote the code test-first, and ran the experiments, and I reviewed every diff and ran every git command myself. I double-checked it constantly: I ran the tests after every session, ran the program myself before every commit, and I pushed back when the AI proposed making genre a small bonus, because I think people name their taste by genre first. The AI also caught its own mistakes when I asked it to check: the worker prompts had the wrong genre count, a report credited me with reasoning that was not mine, and a reason line printed 0.25 as 0.2.

What surprised me is how much five weighted matches and a because line feel like a recommendation. The conflicted profile is the clearest example: a slow sad pop song won a loud profile because two words matched, and the explanation made that feel reasonable even though the numbers said otherwise.

Next I would build the two-cluster profile and grow the catalog, and I would like to replace the typed-in numbers with features measured from audio, so that valence means what the music sounds like instead of what someone imagined.
