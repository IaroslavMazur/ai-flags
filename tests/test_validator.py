"""Tests for flag validation."""

import pytest

from ai_flags.validator import RECOGNIZED_FLAGS, validate_flags


class TestValidateFlags:
    """Test validate_flags() function."""

    @pytest.mark.parametrize(
        "flags,enabled",
        [
            # Individual flags
            (["s"], {"s", "c", "t", "d", "n"}),
            (["c"], {"s", "c", "t", "d", "n"}),
            (["t"], {"s", "c", "t", "d", "n"}),
            (["d"], {"s", "c", "t", "d", "n"}),
            (["n"], {"s", "c", "t", "d", "n"}),
            # Multiple flags
            (["s", "c"], {"s", "c", "t", "d", "n"}),
            (["s", "c", "t", "d", "n"], {"s", "c", "t", "d", "n"}),
            # Empty list is valid (all flags are recognized)
            ([], {"s", "c", "t", "d", "n"}),
            # Subset of enabled flags
            (["s", "c"], {"s", "c"}),
            (["t"], {"t"}),
        ],
    )
    def test_valid_flags(self, flags: list[str], enabled: set[str]) -> None:
        """Test validation of recognized and enabled flags."""
        assert validate_flags(flags, enabled) is True

    @pytest.mark.parametrize(
        "flags,enabled",
        [
            # Unknown flags
            (["x"], {"s", "c", "t", "d", "n"}),
            (["s", "x"], {"s", "c", "t", "d", "n"}),
            (["s", "c", "invalid"], {"s", "c", "t", "d", "n"}),
            (["S"], {"s", "c", "t", "d", "n"}),  # uppercase
            (["1"], {"s", "c", "t", "d", "n"}),  # number
            # Disabled flags (recognized but not enabled)
            (["s"], {"c", "t", "d", "n"}),  # s not enabled
            (["c"], {"s", "t", "d", "n"}),  # c not enabled
            (["s", "c"], {"s"}),  # c not enabled
            (["s", "c", "t"], {"s", "c"}),  # t not enabled
        ],
    )
    def test_invalid_flags(self, flags: list[str], enabled: set[str]) -> None:
        """Test validation of unrecognized or disabled flags."""
        assert validate_flags(flags, enabled) is False


class TestRecognizedFlags:
    """Test RECOGNIZED_FLAGS constant."""

    def test_contains_all_expected_flags(self) -> None:
        """Should contain exactly s, c, t, d, n."""
        assert RECOGNIZED_FLAGS == {"s", "c", "t", "d", "n"}

    def test_is_set_type(self) -> None:
        """Should be a set for efficient lookups."""
        assert isinstance(RECOGNIZED_FLAGS, set)

    def test_has_five_flags(self) -> None:
        """Should have exactly 5 recognized flags."""
        assert len(RECOGNIZED_FLAGS) == 5
