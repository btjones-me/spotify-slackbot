"""Tests for `spotify_slackbot` package."""

import pytest
from assertpy import assert_that
from spotify_slackbot.helpers import extract_spotify_links


@pytest.mark.parametrize(
    "message, expected",
    [
        (
            "Check this album: https://open.spotify.com/album/1abcD2Ef3G4?si=m4RqicAvQPiIa4Snk0S2YA",
            ["https://open.spotify.com/album/1abcD2Ef3G4?si=m4RqicAvQPiIa4Snk0S2YA"],
        ),
        (
            "Listen to this track: https://open.spotify.com/track/3KVU2TkdMgXiiDfTmgSR5u?si=b873bd9d91974300",
            [
                "https://open.spotify.com/track/3KVU2TkdMgXiiDfTmgSR5u?si=b873bd9d91974300"
            ],
        ),
        (
            "Two links: https://open.spotify.com/track/3aXYZ?si=123 https://open.spotify.com/album/4bXYZ?si=456",
            [
                "https://open.spotify.com/track/3aXYZ?si=123",
                "https://open.spotify.com/album/4bXYZ?si=456",
            ],
        ),
        ("No link here", []),
        ("", []),
    ],
)
def test_extract_spotify_links(message, expected):
    result = extract_spotify_links(message)
    assert result == expected
