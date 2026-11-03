"""Diversity re-ranking: keeps one artist from filling the top of the list.
Without it a recommender feeds back more of the same, a filter bubble."""
from __future__ import annotations
from typing import Dict, List, Tuple


def apply_artist_penalty(scored: List[Tuple[Dict, float, List[str]]], penalty: float = 0.5) -> List[Tuple[Dict, float, List[str]]]:
    """Greedy re-rank: walk the list from the top; each song loses penalty × (songs already kept by the same artist) and gains a reason line; return re-sorted."""
    if penalty <= 0:
        return scored
    seen: Dict[str, int] = {}
    result = []
    for song, score, reasons in scored:
        artist = str(song.get("artist") or "").strip().lower()
        repeats = seen.get(artist, 0)
        new_reasons = list(reasons)   # copy: never touch the caller's list
        if repeats:
            deduction = penalty * repeats
            score = round(score - deduction, 4)
            new_reasons.append(f"artist already listed (-{deduction:.2f})")
        result.append((song, score, new_reasons))
        seen[artist] = repeats + 1
    return sorted(result, key=lambda item: item[1], reverse=True)   # stable: ties keep input order
