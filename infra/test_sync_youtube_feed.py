"""Run: uvx --with requests pytest infra/test_sync_youtube_feed.py -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import sync_youtube as sy

ATOM = (
    b'<?xml version="1.0" encoding="UTF-8"?>'
    b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>A video</title></entry></feed>'
)


def test_normal_atom_feed_parses() -> None:
    root = sy.parse_feed(ATOM)
    assert root.find("atom:entry", sy.NS) is not None


@pytest.mark.parametrize("marker", [b"<!DOCTYPE", b"<!ENTITY"])
def test_feed_with_dtd_or_entity_is_refused(marker: bytes) -> None:
    bad = ATOM.replace(b"<feed", marker + b' x [<!ENTITY a "aaaa">]><feed', 1)
    with pytest.raises(ValueError):
        sy.parse_feed(bad)


def test_oversized_feed_is_refused() -> None:
    with pytest.raises(ValueError):
        sy.parse_feed(ATOM + b" " * sy.MAX_FEED_BYTES)
