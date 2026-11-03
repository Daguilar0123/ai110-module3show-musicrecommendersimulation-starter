"""Output formatting: renders ranked recommendations as a tabulate grid."""
from __future__ import annotations
import textwrap
from typing import Dict, List, Tuple

from tabulate import tabulate

WHY_WIDTH = 60   # reasons wrap at about this many characters


def format_table(results: List[Tuple[Dict, float, str]]) -> str:
    """Return a tabulate grid: rank, title, artist, score (2 dp), reasons."""
    rows = [
        [rank, song["title"], song["artist"], f"{score:.2f}", textwrap.fill(explanation, width=WHY_WIDTH)]
        for rank, (song, score, explanation) in enumerate(results, start=1)
    ]
    return tabulate(rows, headers=["#", "Title", "Artist", "Score", "Why"], tablefmt="github", disable_numparse=True)
