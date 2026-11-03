# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
