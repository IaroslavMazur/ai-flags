"""Flag validation logic."""

# Flag registry - all recognized flags
RECOGNIZED_FLAGS = {"s", "c", "t", "d", "n"}


def validate_flags(flags: list[str], enabled_flags: set[str]) -> bool:
    """Validate that all flags are recognized and enabled.

    Args:
        flags: List of flag letters (e.g., ["s", "c"])
        enabled_flags: Set of enabled flag letters from config

    Returns:
        True if all flags are valid and enabled, False otherwise
    """
    # Check all flags are recognized
    if not all(flag in RECOGNIZED_FLAGS for flag in flags):
        return False

    # Check all flags are enabled in config
    if not all(flag in enabled_flags for flag in flags):
        return False

    return True
