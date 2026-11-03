"""Output formatting: renders ranked recommendations as a tabulate grid."""
from __future__ import annotations
from typing import Dict, List, Tuple


def format_table(results: List[Tuple[Dict, float, str]]) -> str:
    """Return a tabulate grid: rank, title, artist, score (2 dp), reasons."""
    raise NotImplementedError  # S5
