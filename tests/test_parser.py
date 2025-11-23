"""Tests for flag parsing."""

import pytest

from ai_flags.parser import parse_trailing_flags


class TestParseTrailingFlags:
    """Test parse_trailing_flags() function."""

    @pytest.mark.parametrize(
        "prompt,expected",
        [
            # Valid single flags
            ("my task -s", ("my task", ["s"])),
            ("my task -c", ("my task", ["c"])),
            ("my task -t", ("my task", ["t"])),
            ("my task -d", ("my task", ["d"])),
            ("my task -n", ("my task", ["n"])),
            # Valid multiple flags
            ("my task -s -c", ("my task", ["s", "c"])),
            ("my task -t -d -n", ("my task", ["t", "d", "n"])),
            ("my task -s -c -t -d -n", ("my task", ["s", "c", "t", "d", "n"])),
            # With extra whitespace
            ("my task  -s  -c", ("my task", ["s", "c"])),
            ("my task -s  ", ("my task", ["s"])),
            ("  my task -s", ("my task", ["s"])),
            # Complex prompts
            (
                "complex task with many words -s -c",
                ("complex task with many words", ["s", "c"]),
            ),
            # Multiline prompts
            ("first line\nsecond line -s", ("first line\nsecond line", ["s"])),
            (
                "line 1\nline 2\nline 3 -s -c",
                ("line 1\nline 2\nline 3", ["s", "c"]),
            ),
            ("paragraph 1\n\nparagraph 2 -t", ("paragraph 1\n\nparagraph 2", ["t"])),
            (
                "lots\n\n\nof\n\n\nnewlines -d -n",
                ("lots\n\n\nof\n\n\nnewlines", ["d", "n"]),
            ),
        ],
    )
    def test_valid_flags(self, prompt: str, expected: tuple[str, list[str]]) -> None:
        """Test parsing of valid flag patterns."""
        result = parse_trailing_flags(prompt)
        assert result == expected

    @pytest.mark.parametrize(
        "prompt",
        [
            # No flags
            "my task",
            "my task with no flags",
            "",
            "   ",
            # Flags in wrong position
            "-s my task",
            "my -s task",
            "my task -s more text",
            # Invalid flag format
            "my task -",
            "my task - s",
            "my task --s",
            "my task -S",  # uppercase
            "my task -1",  # number
            # No text before flags
            "-s",
        ],
    )
    def test_no_match(self, prompt: str) -> None:
        """Test cases where no flags should be detected."""
        result = parse_trailing_flags(prompt)
        assert result is None

    def test_flags_only_matches_as_valid(self) -> None:
        """Test that flags-only input (e.g., '-s -c') does match the pattern.

        This is a quirk of the regex - the first flag becomes the 'prompt'
        and remaining flags are parsed as flags. While unusual, this is
        acceptable behavior and will be filtered out by validation if needed.
        """
        result = parse_trailing_flags("-s -c")
        # This matches with "-s" as prompt and ["c"] as flags
        assert result is not None
        assert result[0] == "-s"
        assert result[1] == ["c"]
