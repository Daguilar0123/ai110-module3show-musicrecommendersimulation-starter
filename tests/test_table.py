"""Tests for the tabulate summary table (Challenge 4)."""
from src.formatting import format_table


def fake_results(n=5):
    return [({"id": i, "title": f"Song {i}", "artist": f"Artist {i}"}, 4.0 - i * 0.25, f"genre match (+2.0); reason {i}")
            for i in range(1, n + 1)]


def test_table_has_header_and_rows():
    lines = format_table(fake_results(5)).splitlines()
    assert "Title" in lines[0] and "Why" in lines[0]
    assert len(lines) == 2 + 5   # header, separator, five rows


def test_table_includes_reasons():
    table = format_table(fake_results(5))
    for i in range(1, 6):
        assert f"reason {i}" in table


def test_table_returns_string_not_prints(capsys):
    out = format_table(fake_results(5))
    assert isinstance(out, str)
    assert capsys.readouterr().out == ""
