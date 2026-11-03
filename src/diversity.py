"""Diversity re-ranking: keeps one artist from filling the top of the list."""
from __future__ import annotations
from typing import Dict, List, Tuple


def apply_artist_penalty(scored: List[Tuple[Dict, float, List[str]]], penalty: float = 0.5) -> List[Tuple[Dict, float, List[str]]]:
    """Greedy re-rank: walk the list from the top; each song loses penalty × (songs already kept by the same artist) and gains a reason line; return re-sorted."""
    raise NotImplementedError  # S6
